"""
NOIZY Fish — HTTP API
======================

FastAPI endpoints for NOIZY Fish registry.
All endpoints return JSON.

Endpoints:
- POST   /creators                  — Register creator
- GET    /creators/{id}             — Get creator
- GET    /creators/search           — Search creators
- POST   /consent/check             — Check consent (core query!)
- PUT    /creators/{id}/consent     — Update consent rule
- POST   /works                     — Register work
- GET    /works/{id}                — Get work
- POST   /inquiries                 — Submit licensing inquiry
- GET    /inquiries                 — List inquiries
- GET    /stats                     — Registry stats
- GET    /c2pa/{work_id}            — Export C2PA manifest
- GET    /health                    — Health check

Run: uvicorn gabriel.noizy_fish.api:app --reload --port 8765
"""

import os
from datetime import datetime
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .registry import NoizyFishDB
from .identity.creator_passport import (
    CreatorPassport,
    CreatorIdentity,
    CreatorType,
    VerificationStatus,
    ConsentRegistry,
    ConsentRule,
    UseCategory,
    ConsentDecision,
    CompensationTerms,
    CompensationType
)
from .standards import IPI, ISNI, NoizyID


# ═══════════════════════════════════════════════════════════════════════════
# FastAPI App
# ═══════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="NOIZY Fish Registry",
    description="Creator consent registry for the music industry",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database
DB_PATH = os.environ.get("NOIZY_FISH_DB", "noizy_fish.db")
db = NoizyFishDB(DB_PATH)


# ═══════════════════════════════════════════════════════════════════════════
# Request/Response Models
# ═══════════════════════════════════════════════════════════════════════════

class RegisterCreatorRequest(BaseModel):
    display_name: str = Field(..., description="Public/artist name")
    creator_types: list[str] = Field(default=["performer"], description="Creator types")
    ipi_number: Optional[str] = Field(None, description="IPI number (11 digits)")
    isni_number: Optional[str] = Field(None, description="ISNI number (16 digits)")
    pro_membership: Optional[str] = Field(None, description="PRO: ASCAP, BMI, etc.")
    default_consent: str = Field(default="requires_approval", description="Default consent decision")


class CreatorResponse(BaseModel):
    creator_id: str
    noizy_id: str
    display_name: str
    creator_types: list[str]
    ipi_number: Optional[str]
    isni_number: Optional[str]
    pro_membership: Optional[str]
    verification_status: str
    consent_rules: list[dict]
    created_at: str
    updated_at: str


class ConsentCheckRequest(BaseModel):
    creator_id: str = Field(..., description="Creator ID")
    use_category: str = Field(..., description="Use type: streaming, sync_film, ai_training, etc.")
    requestor: Optional[str] = Field(None, description="Requesting party name")
    context: Optional[str] = Field(None, description="Context/description")
    territory: str = Field(default="WW", description="ISO territory code")
    offered_amount: Optional[float] = Field(None, description="Offered compensation")


class ConsentCheckResponse(BaseModel):
    creator_id: str
    use_category: str
    decision: str
    reasons: list[str]
    compensation: Optional[dict]


class UpdateConsentRequest(BaseModel):
    use_category: str = Field(..., description="Use category")
    decision: str = Field(..., description="Decision: allowed, denied, etc.")
    minimum_amount: Optional[float] = Field(None, description="Minimum compensation")
    excluded_parties: Optional[list[str]] = Field(None, description="Excluded parties")
    excluded_contexts: Optional[list[str]] = Field(None, description="Excluded contexts")


class RegisterWorkRequest(BaseModel):
    creator_id: str = Field(..., description="Creator ID")
    title: str = Field(..., description="Work title")
    work_type: str = Field(..., description="Type: recording, composition, voice")
    isrc: Optional[str] = Field(None, description="ISRC code")
    iswc: Optional[str] = Field(None, description="ISWC code")
    format: Optional[str] = Field(None, description="Format: audio/wav, etc.")


class WorkResponse(BaseModel):
    work_id: str
    noizy_work_id: str
    creator_id: str
    work_type: str
    title: str
    isrc: Optional[str]
    iswc: Optional[str]
    format: Optional[str]
    created_at: str


class InquiryRequest(BaseModel):
    creator_id: str = Field(..., description="Creator ID")
    requestor_name: str = Field(..., description="Requesting party")
    requestor_email: Optional[str] = Field(None, description="Requestor email")
    use_category: str = Field(..., description="Use category")
    work_id: Optional[str] = Field(None, description="Work ID")
    territory: str = Field(default="WW", description="Territory")
    context: Optional[str] = Field(None, description="Context")
    offered_amount: Optional[float] = Field(None, description="Offered amount")


class InquiryResponse(BaseModel):
    inquiry_id: str
    status: str
    decision: str
    reasons: list[str]
    compensation: Optional[dict]
    requestor: str
    use_category: str
    message: str


# ═══════════════════════════════════════════════════════════════════════════
# Endpoints
# ═══════════════════════════════════════════════════════════════════════════

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "noizy-fish", "timestamp": datetime.utcnow().isoformat()}


@app.get("/stats")
async def get_stats():
    """Get registry statistics."""
    stats = db.get_stats()
    valid, issues = db.verify_transaction_log()
    return {
        **stats,
        "transaction_log_valid": valid,
        "issues": issues if not valid else None
    }


# ─────────────────────────────────────────────────────────────────────────────
# Creator Endpoints
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/creators", response_model=dict)
async def register_creator(request: RegisterCreatorRequest):
    """Register a new creator."""
    passport = CreatorPassport()

    passport.identity.display_name = request.display_name
    passport.identity.creator_types = [
        CreatorType(t) for t in request.creator_types
    ]

    if request.ipi_number:
        try:
            passport.identity.ipi_number = IPI.parse(request.ipi_number)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid IPI: {e}")

    if request.isni_number:
        try:
            passport.identity.isni_number = ISNI.parse(request.isni_number)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid ISNI: {e}")

    passport.identity.pro_membership = request.pro_membership
    passport.consent.default_decision = ConsentDecision(request.default_consent)

    creator_id = db.save_creator(passport)

    db.log_transaction(
        "creator_registered",
        {
            "creator_id": creator_id,
            "display_name": passport.identity.display_name,
            "types": [t.value for t in passport.identity.creator_types]
        },
        entity_id=creator_id,
        entity_type="creator"
    )

    return {
        "success": True,
        "creator_id": creator_id,
        "noizy_id": str(passport.identity.noizy_id),
        "display_name": passport.identity.display_name
    }


@app.get("/creators/{creator_id}")
async def get_creator(creator_id: str):
    """Get creator by ID."""
    import json
    creator = db.get_creator(creator_id)

    if not creator:
        creator = db.get_creator_by_noizy_id(creator_id)

    if not creator:
        raise HTTPException(status_code=404, detail="Creator not found")

    rules = db.get_consent_rules(creator["creator_id"])

    return {
        "creator_id": creator["creator_id"],
        "noizy_id": creator["noizy_id"],
        "display_name": creator["display_name"],
        "creator_types": json.loads(creator["creator_types"]),
        "ipi_number": creator["ipi_number"],
        "isni_number": creator["isni_number"],
        "pro_membership": creator["pro_membership"],
        "verification_status": creator["verification_status"],
        "consent_rules": [
            {
                "use_category": r["use_category"],
                "decision": r["decision"],
                "min_compensation": r["min_compensation"]
            }
            for r in rules
        ],
        "created_at": creator["created_at"],
        "updated_at": creator["updated_at"]
    }


@app.get("/creators/search/")
async def search_creators(
    q: Optional[str] = Query(None, description="Search query"),
    type: Optional[str] = Query(None, description="Creator type"),
    limit: int = Query(50, description="Max results")
):
    """Search creators."""
    import json
    results = db.search_creators(query=q, creator_type=type, limit=limit)

    return {
        "count": len(results),
        "creators": [
            {
                "creator_id": c["creator_id"],
                "noizy_id": c["noizy_id"],
                "display_name": c["display_name"],
                "creator_types": json.loads(c["creator_types"]),
                "verification_status": c["verification_status"]
            }
            for c in results
        ]
    }


# ─────────────────────────────────────────────────────────────────────────────
# Consent Endpoints
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/consent/check", response_model=ConsentCheckResponse)
async def check_consent(request: ConsentCheckRequest):
    """
    Check consent — THE CORE QUERY.
    This is what gets called for every licensing inquiry.
    """
    result = db.check_consent(
        creator_id=request.creator_id,
        use_category=request.use_category,
        requestor=request.requestor,
        context=request.context,
        territory=request.territory,
        offered_amount=request.offered_amount
    )

    if result.get("decision") == "error":
        raise HTTPException(status_code=404, detail=result["reasons"][0])

    return ConsentCheckResponse(
        creator_id=request.creator_id,
        use_category=request.use_category,
        decision=result["decision"],
        reasons=result["reasons"],
        compensation=result.get("compensation")
    )


@app.put("/creators/{creator_id}/consent")
async def update_consent_rule(creator_id: str, request: UpdateConsentRequest):
    """Update consent rule for a creator."""
    import json

    creator = db.get_creator(creator_id)
    if not creator:
        raise HTTPException(status_code=404, detail="Creator not found")

    rule = ConsentRule(
        use_category=UseCategory(request.use_category),
        decision=ConsentDecision(request.decision)
    )

    if request.minimum_amount:
        rule.compensation = CompensationTerms(
            compensation_type=CompensationType.FLAT_FEE,
            minimum_amount=request.minimum_amount
        )

    if request.excluded_parties:
        rule.excluded_parties = request.excluded_parties

    if request.excluded_contexts:
        rule.excluded_contexts = request.excluded_contexts

    with db._get_conn() as conn:
        db._save_consent_rule(conn, creator_id, rule)

    db.log_transaction(
        "consent_rule_updated",
        {
            "creator_id": creator_id,
            "use_category": request.use_category,
            "decision": request.decision,
            "minimum_amount": request.minimum_amount
        },
        entity_id=creator_id,
        entity_type="consent_rule"
    )

    return {
        "success": True,
        "creator_id": creator_id,
        "use_category": request.use_category,
        "decision": request.decision
    }


# ─────────────────────────────────────────────────────────────────────────────
# Work Endpoints
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/works", response_model=WorkResponse)
async def register_work(request: RegisterWorkRequest):
    """Register a work (recording, composition, voice asset)."""
    work_id = str(uuid4())
    work_type = request.work_type

    type_prefix = {"recording": "REC", "composition": "WK", "voice": "VOC"}.get(work_type, "WK")
    noizy_work_id = f"NZ-{type_prefix}-{datetime.utcnow().strftime('%Y%m%d')}-{work_id[:8].upper()}"

    db.save_work(
        work_id=work_id,
        noizy_work_id=noizy_work_id,
        creator_id=request.creator_id,
        work_type=work_type,
        title=request.title,
        isrc=request.isrc,
        iswc=request.iswc,
        format=request.format
    )

    db.log_transaction(
        "work_registered",
        {
            "work_id": work_id,
            "noizy_work_id": noizy_work_id,
            "creator_id": request.creator_id,
            "title": request.title
        },
        entity_id=work_id,
        entity_type="work"
    )

    return WorkResponse(
        work_id=work_id,
        noizy_work_id=noizy_work_id,
        creator_id=request.creator_id,
        work_type=work_type,
        title=request.title,
        isrc=request.isrc,
        iswc=request.iswc,
        format=request.format,
        created_at=datetime.utcnow().isoformat()
    )


@app.get("/works/{work_id}")
async def get_work(work_id: str):
    """Get work by ID."""
    work = db.get_work(work_id)

    if not work:
        raise HTTPException(status_code=404, detail="Work not found")

    return {
        "work_id": work["work_id"],
        "noizy_work_id": work["noizy_work_id"],
        "creator_id": work["creator_id"],
        "work_type": work["work_type"],
        "title": work["title"],
        "isrc": work["isrc"],
        "iswc": work["iswc"],
        "format": work["format"],
        "created_at": work["created_at"]
    }


@app.get("/creators/{creator_id}/works")
async def get_creator_works(creator_id: str):
    """Get all works by a creator."""
    works = db.get_works_by_creator(creator_id)

    return {
        "count": len(works),
        "works": [
            {
                "work_id": w["work_id"],
                "noizy_work_id": w["noizy_work_id"],
                "work_type": w["work_type"],
                "title": w["title"],
                "isrc": w["isrc"],
                "iswc": w["iswc"]
            }
            for w in works
        ]
    }


# ─────────────────────────────────────────────────────────────────────────────
# Inquiry Endpoints
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/inquiries", response_model=InquiryResponse)
async def submit_inquiry(request: InquiryRequest):
    """Submit a full licensing inquiry."""
    # Check consent
    consent_result = db.check_consent(
        creator_id=request.creator_id,
        use_category=request.use_category,
        requestor=request.requestor_name,
        context=request.context,
        territory=request.territory,
        offered_amount=request.offered_amount
    )

    if consent_result.get("decision") == "error":
        raise HTTPException(status_code=404, detail=consent_result["reasons"][0])

    # Log inquiry
    inquiry_id = db.log_inquiry(
        creator_id=request.creator_id,
        requestor_name=request.requestor_name,
        use_category=request.use_category,
        decision=consent_result["decision"],
        reasons=consent_result["reasons"],
        work_id=request.work_id,
        requestor_email=request.requestor_email,
        territory=request.territory,
        context=request.context,
        offered_amount=request.offered_amount
    )

    # Log transaction
    db.log_transaction(
        "inquiry_submitted",
        {
            "inquiry_id": inquiry_id,
            "creator_id": request.creator_id,
            "requestor": request.requestor_name,
            "decision": consent_result["decision"]
        },
        entity_id=inquiry_id,
        entity_type="inquiry"
    )

    # Determine status
    decision = consent_result["decision"]
    if decision in ["allowed", "allowed_terms"]:
        status = "APPROVED"
    elif decision in ["requires_approval", "negotiable"]:
        status = "PENDING_REVIEW"
    else:
        status = "DENIED"

    return InquiryResponse(
        inquiry_id=inquiry_id,
        status=status,
        decision=decision,
        reasons=consent_result["reasons"],
        compensation=consent_result.get("compensation"),
        requestor=request.requestor_name,
        use_category=request.use_category,
        message=f"Inquiry {status}: {consent_result['reasons'][0] if consent_result['reasons'] else decision}"
    )


@app.get("/inquiries")
async def list_inquiries(
    creator_id: Optional[str] = Query(None, description="Filter by creator"),
    decision: Optional[str] = Query(None, description="Filter by decision"),
    limit: int = Query(100, description="Max results")
):
    """List licensing inquiries."""
    import json
    inquiries = db.get_inquiries(creator_id=creator_id, decision=decision, limit=limit)

    return {
        "count": len(inquiries),
        "inquiries": [
            {
                "inquiry_id": i["inquiry_id"],
                "creator_id": i["creator_id"],
                "requestor_name": i["requestor_name"],
                "use_category": i["use_category"],
                "decision": i["decision"],
                "offered_amount": i["offered_amount"],
                "created_at": i["created_at"]
            }
            for i in inquiries
        ]
    }


# ─────────────────────────────────────────────────────────────────────────────
# C2PA Export
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/c2pa/{work_id}")
async def export_c2pa_manifest(work_id: str):
    """Export C2PA manifest for a work."""
    import json

    work = db.get_work(work_id)
    if not work:
        raise HTTPException(status_code=404, detail="Work not found")

    creator = db.get_creator(work["creator_id"])
    if not creator:
        raise HTTPException(status_code=404, detail="Creator not found")

    # Build C2PA manifest
    manifest = {
        "@context": "https://c2pa.org/manifest/1",
        "claim_generator": "NOIZY Fish/1.0",
        "dc:title": work["title"],
        "dc:format": work["format"] or "audio/wav",
        "instanceID": f"urn:uuid:{work['work_id']}",
        "assertions": {
            "c2pa.actions": [
                {
                    "action": "c2pa.created",
                    "when": work["created_at"],
                    "softwareAgent": {"name": "NOIZY Fish"}
                }
            ],
            "noizy.creator": {
                "name": creator["display_name"],
                "identifier": [
                    {"type": "noizy", "value": creator["noizy_id"]},
                    {"type": "ipi", "value": creator["ipi_number"]} if creator["ipi_number"] else None,
                    {"type": "isni", "value": creator["isni_number"]} if creator["isni_number"] else None
                ],
                "verified": creator["verification_status"] == "fully_verified"
            },
            "noizy.consent": {
                "registry_id": creator["creator_id"],
                "default_decision": json.loads(creator["passport_data"]).get("consent", {}).get("default_decision")
            }
        },
        "noizy": {
            "work_id": work["noizy_work_id"],
            "isrc": work["isrc"],
            "iswc": work["iswc"],
            "creator_id": creator["creator_id"]
        }
    }

    # Clean up None values
    manifest["assertions"]["noizy.creator"]["identifier"] = [
        i for i in manifest["assertions"]["noizy.creator"]["identifier"] if i
    ]

    return manifest


# ─────────────────────────────────────────────────────────────────────────────
# Batch Operations
# ─────────────────────────────────────────────────────────────────────────────

class BatchConsentCheckRequest(BaseModel):
    checks: list[ConsentCheckRequest]


@app.post("/consent/check/batch")
async def batch_check_consent(request: BatchConsentCheckRequest):
    """
    Batch consent check — check multiple inquiries at once.
    Useful for DSPs checking catalog permissions.
    """
    results = []

    for check in request.checks:
        result = db.check_consent(
            creator_id=check.creator_id,
            use_category=check.use_category,
            requestor=check.requestor,
            context=check.context,
            territory=check.territory,
            offered_amount=check.offered_amount
        )

        results.append({
            "creator_id": check.creator_id,
            "use_category": check.use_category,
            "decision": result["decision"],
            "reasons": result["reasons"]
        })

    # Summary
    allowed = sum(1 for r in results if r["decision"] in ["allowed", "allowed_terms"])
    denied = sum(1 for r in results if r["decision"] == "denied")
    pending = len(results) - allowed - denied

    return {
        "total": len(results),
        "summary": {
            "allowed": allowed,
            "denied": denied,
            "pending_review": pending
        },
        "results": results
    }


# ─────────────────────────────────────────────────────────────────────────────
# Real-time Events (SSE + WebSocket)
# ─────────────────────────────────────────────────────────────────────────────

from .realtime import create_sse_routes, create_websocket_routes

# Add SSE routes (/events, /events/status)
create_sse_routes(app)

# Add WebSocket routes (/ws)
create_websocket_routes(app)


# ─────────────────────────────────────────────────────────────────────────────
# Embeddable Widget
# ─────────────────────────────────────────────────────────────────────────────

from .widget import create_widget_routes

# Add widget routes (/widget/embed.js, /widget/demo, etc.)
create_widget_routes(app)


# ─────────────────────────────────────────────────────────────────────────────
# Analytics Endpoints
# ─────────────────────────────────────────────────────────────────────────────

from .analytics import AnalyticsEngine


@app.get("/analytics/summary")
async def get_analytics_summary():
    """Get analytics summary report."""
    analytics = AnalyticsEngine(db)
    report = analytics.generate_report("summary")
    return report


@app.get("/analytics/ai")
async def get_ai_analytics():
    """Get AI consent analytics."""
    analytics = AnalyticsEngine(db)
    return analytics.get_ai_consent_stats()


@app.get("/analytics/categories")
async def get_category_analytics():
    """Get category breakdown."""
    analytics = AnalyticsEngine(db)
    return {
        "categories": analytics.get_category_breakdown()
    }


@app.get("/analytics/creator/{creator_id}")
async def get_creator_analytics(creator_id: str):
    """Get analytics for a specific creator."""
    analytics = AnalyticsEngine(db)
    return analytics.get_creator_metrics(creator_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8765)
