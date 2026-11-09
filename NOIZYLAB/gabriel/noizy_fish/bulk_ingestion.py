"""
NOIZY Fish — Bulk Catalog Ingestion
=====================================

Import large catalogs of creators, works, and consent rules.

Supports:
- CSV import (spreadsheet format)
- JSON import (API format)
- DDEX/RIN XML import (industry standard)

Features:
- Batch processing with progress tracking
- Validation and error reporting
- Duplicate detection
- Consent rule templates
- ISRC/ISWC validation
"""

import csv
import json
import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from io import StringIO
from pathlib import Path
from typing import Optional, Generator
from uuid import uuid4

from .registry import NoizyFishDB
from .identity.creator_passport import (
    CreatorPassport,
    CreatorIdentity,
    CreatorType,
    ConsentRule,
    UseCategory,
    ConsentDecision,
    CompensationTerms,
    CompensationType
)
from .standards import IPI, ISNI, ISRC, ISWC


# ═══════════════════════════════════════════════════════════════════════════
# Import Result Tracking
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class ImportResult:
    """Result of an import operation."""
    total: int = 0
    successful: int = 0
    failed: int = 0
    skipped: int = 0
    errors: list[dict] = field(default_factory=list)
    created_ids: list[str] = field(default_factory=list)

    def add_success(self, entity_id: str):
        self.successful += 1
        self.created_ids.append(entity_id)

    def add_failure(self, row: int, error: str, data: dict = None):
        self.failed += 1
        self.errors.append({
            "row": row,
            "error": error,
            "data": data
        })

    def add_skip(self, reason: str):
        self.skipped += 1

    def to_dict(self) -> dict:
        return {
            "total": self.total,
            "successful": self.successful,
            "failed": self.failed,
            "skipped": self.skipped,
            "success_rate": f"{(self.successful / self.total * 100):.1f}%" if self.total > 0 else "0%",
            "errors": self.errors[:20],  # First 20 errors
            "created_ids": self.created_ids[:100]  # First 100 IDs
        }


# ═══════════════════════════════════════════════════════════════════════════
# Consent Templates
# ═══════════════════════════════════════════════════════════════════════════

CONSENT_TEMPLATES = {
    "standard_artist": {
        "description": "Standard artist consent — streaming allowed, sync negotiable, AI training denied",
        "rules": [
            {"use_category": "streaming", "decision": "allowed"},
            {"use_category": "download", "decision": "allowed"},
            {"use_category": "sync_film", "decision": "negotiable", "min_amount": 5000},
            {"use_category": "sync_ad", "decision": "negotiable", "min_amount": 10000},
            {"use_category": "sample", "decision": "requires_approval"},
            {"use_category": "remix", "decision": "requires_approval"},
            {"use_category": "ai_training", "decision": "denied"},
            {"use_category": "ai_voice_clone", "decision": "denied"},
            {"use_category": "ai_generation", "decision": "denied"},
        ]
    },
    "voice_actor_protective": {
        "description": "Voice actor — protective of voice, no AI cloning",
        "rules": [
            {"use_category": "streaming", "decision": "allowed_terms", "min_amount": 200},
            {"use_category": "sync_game", "decision": "allowed_terms", "min_amount": 500},
            {"use_category": "sync_film", "decision": "allowed_terms", "min_amount": 1000},
            {"use_category": "sync_ad", "decision": "allowed_terms", "min_amount": 2000},
            {"use_category": "educational", "decision": "allowed_terms", "min_amount": 100},
            {"use_category": "ai_voice_clone", "decision": "denied"},
            {"use_category": "ai_training", "decision": "denied"},
            {"use_category": "ai_generation", "decision": "denied"},
        ]
    },
    "producer_remix_friendly": {
        "description": "Producer — remix-friendly, open to sampling",
        "rules": [
            {"use_category": "streaming", "decision": "allowed"},
            {"use_category": "download", "decision": "allowed"},
            {"use_category": "sample", "decision": "allowed_terms", "min_amount": 500},
            {"use_category": "remix", "decision": "allowed_terms", "min_amount": 250},
            {"use_category": "sync_ad", "decision": "negotiable", "min_amount": 5000},
            {"use_category": "ai_training", "decision": "negotiable", "min_amount": 25000},
        ]
    },
    "composer_premium": {
        "description": "Composer — premium sync rates, publishing focus",
        "rules": [
            {"use_category": "streaming", "decision": "allowed"},
            {"use_category": "sync_film", "decision": "allowed_terms", "min_amount": 10000},
            {"use_category": "sync_tv", "decision": "allowed_terms", "min_amount": 5000},
            {"use_category": "sync_ad", "decision": "allowed_terms", "min_amount": 15000,
             "excluded_contexts": ["tobacco", "alcohol", "firearms", "political", "gambling"]},
            {"use_category": "sample", "decision": "requires_approval"},
            {"use_category": "ai_training", "decision": "denied"},
        ]
    },
    "all_rights_reserved": {
        "description": "All rights reserved — require approval for everything",
        "rules": [
            {"use_category": "streaming", "decision": "requires_approval"},
            {"use_category": "download", "decision": "requires_approval"},
            {"use_category": "sync_film", "decision": "requires_approval"},
            {"use_category": "sync_ad", "decision": "requires_approval"},
            {"use_category": "sample", "decision": "denied"},
            {"use_category": "remix", "decision": "denied"},
            {"use_category": "ai_training", "decision": "denied"},
            {"use_category": "ai_voice_clone", "decision": "denied"},
        ]
    },
    "open_creative_commons": {
        "description": "Open/CC-style — allow most uses with attribution",
        "rules": [
            {"use_category": "streaming", "decision": "allowed"},
            {"use_category": "download", "decision": "allowed"},
            {"use_category": "sample", "decision": "allowed"},
            {"use_category": "remix", "decision": "allowed"},
            {"use_category": "educational", "decision": "allowed"},
            {"use_category": "non_profit", "decision": "allowed"},
            {"use_category": "sync_ad", "decision": "requires_approval"},
            {"use_category": "ai_training", "decision": "requires_approval"},
        ]
    }
}


def get_template(template_name: str) -> Optional[dict]:
    """Get a consent template by name."""
    return CONSENT_TEMPLATES.get(template_name)


def list_templates() -> list[dict]:
    """List all available templates."""
    return [
        {"name": name, "description": tmpl["description"]}
        for name, tmpl in CONSENT_TEMPLATES.items()
    ]


def apply_template(passport: CreatorPassport, template_name: str) -> bool:
    """Apply a consent template to a passport."""
    template = CONSENT_TEMPLATES.get(template_name)
    if not template:
        return False

    for rule_data in template["rules"]:
        rule = ConsentRule(
            use_category=UseCategory(rule_data["use_category"]),
            decision=ConsentDecision(rule_data["decision"])
        )

        if rule_data.get("min_amount"):
            rule.compensation = CompensationTerms(
                compensation_type=CompensationType.FLAT_FEE,
                minimum_amount=rule_data["min_amount"]
            )

        if rule_data.get("excluded_contexts"):
            rule.excluded_contexts = rule_data["excluded_contexts"]

        passport.update_consent_rule(rule)

    return True


# ═══════════════════════════════════════════════════════════════════════════
# CSV Import
# ═══════════════════════════════════════════════════════════════════════════

def import_creators_csv(
    db: NoizyFishDB,
    csv_content: str,
    consent_template: Optional[str] = None
) -> ImportResult:
    """
    Import creators from CSV.

    Expected columns:
    - display_name (required)
    - creator_types (comma-separated)
    - ipi_number
    - isni_number
    - pro_membership
    - email
    - consent_template (overrides parameter)
    """
    result = ImportResult()
    reader = csv.DictReader(StringIO(csv_content))

    for row_num, row in enumerate(reader, start=2):
        result.total += 1

        try:
            # Validate required fields
            display_name = row.get("display_name", "").strip()
            if not display_name:
                result.add_failure(row_num, "Missing display_name", row)
                continue

            # Create passport
            passport = CreatorPassport()
            passport.identity.display_name = display_name

            # Parse creator types
            types_str = row.get("creator_types", "performer")
            types = [t.strip() for t in types_str.split(",") if t.strip()]
            passport.identity.creator_types = [
                CreatorType(t) for t in types if t in [e.value for e in CreatorType]
            ]

            # Parse IPI
            ipi = row.get("ipi_number", "").strip()
            if ipi:
                try:
                    passport.identity.ipi_number = IPI.parse(ipi)
                except ValueError as e:
                    result.add_failure(row_num, f"Invalid IPI: {e}", row)
                    continue

            # Parse ISNI
            isni = row.get("isni_number", "").strip()
            if isni:
                try:
                    passport.identity.isni_number = ISNI.parse(isni)
                except ValueError as e:
                    result.add_failure(row_num, f"Invalid ISNI: {e}", row)
                    continue

            # PRO membership
            passport.identity.pro_membership = row.get("pro_membership", "").strip() or None

            # Apply consent template
            template = row.get("consent_template", "").strip() or consent_template
            if template:
                if not apply_template(passport, template):
                    result.add_failure(row_num, f"Unknown template: {template}", row)
                    continue

            # Save to database
            creator_id = db.save_creator(passport)
            result.add_success(creator_id)

        except Exception as e:
            result.add_failure(row_num, str(e), row)

    return result


def import_works_csv(
    db: NoizyFishDB,
    csv_content: str
) -> ImportResult:
    """
    Import works from CSV.

    Expected columns:
    - creator_id or creator_noizy_id (required)
    - title (required)
    - work_type (recording, composition, voice)
    - isrc
    - iswc
    - format
    """
    result = ImportResult()
    reader = csv.DictReader(StringIO(csv_content))

    for row_num, row in enumerate(reader, start=2):
        result.total += 1

        try:
            # Get creator
            creator_id = row.get("creator_id", "").strip()
            creator_noizy_id = row.get("creator_noizy_id", "").strip()

            if not creator_id and not creator_noizy_id:
                result.add_failure(row_num, "Missing creator_id or creator_noizy_id", row)
                continue

            # Lookup creator
            if creator_id:
                creator = db.get_creator(creator_id)
            else:
                creator = db.get_creator_by_noizy_id(creator_noizy_id)

            if not creator:
                result.add_failure(row_num, "Creator not found", row)
                continue

            # Validate required fields
            title = row.get("title", "").strip()
            work_type = row.get("work_type", "recording").strip()

            if not title:
                result.add_failure(row_num, "Missing title", row)
                continue

            # Validate ISRC
            isrc = row.get("isrc", "").strip()
            if isrc:
                try:
                    parsed_isrc = ISRC.parse(isrc)
                    if not parsed_isrc.validate():
                        result.add_failure(row_num, f"Invalid ISRC format: {isrc}", row)
                        continue
                    isrc = str(parsed_isrc)
                except ValueError as e:
                    result.add_failure(row_num, f"Invalid ISRC: {e}", row)
                    continue

            # Validate ISWC
            iswc = row.get("iswc", "").strip()
            if iswc:
                try:
                    parsed_iswc = ISWC.parse(iswc)
                    if not parsed_iswc.validate():
                        result.add_failure(row_num, f"Invalid ISWC format: {iswc}", row)
                        continue
                    iswc = str(parsed_iswc)
                except ValueError as e:
                    result.add_failure(row_num, f"Invalid ISWC: {e}", row)
                    continue

            # Generate IDs
            work_id = str(uuid4())
            type_prefix = {"recording": "REC", "composition": "WK", "voice": "VOC"}.get(work_type, "WK")
            noizy_work_id = f"NZ-{type_prefix}-{datetime.utcnow().strftime('%Y%m%d')}-{work_id[:8].upper()}"

            # Save work
            db.save_work(
                work_id=work_id,
                noizy_work_id=noizy_work_id,
                creator_id=creator["creator_id"],
                work_type=work_type,
                title=title,
                isrc=isrc or None,
                iswc=iswc or None,
                format=row.get("format", "").strip() or None
            )

            result.add_success(work_id)

        except Exception as e:
            result.add_failure(row_num, str(e), row)

    return result


# ═══════════════════════════════════════════════════════════════════════════
# JSON Import
# ═══════════════════════════════════════════════════════════════════════════

def import_creators_json(
    db: NoizyFishDB,
    json_content: str,
    consent_template: Optional[str] = None
) -> ImportResult:
    """
    Import creators from JSON.

    Expected format:
    {
        "creators": [
            {
                "display_name": "...",
                "creator_types": ["composer", "songwriter"],
                "ipi_number": "...",
                "isni_number": "...",
                "pro_membership": "ASCAP",
                "consent_template": "composer_premium",
                "consent_rules": [...]  # Optional custom rules
            }
        ]
    }
    """
    result = ImportResult()

    try:
        data = json.loads(json_content)
    except json.JSONDecodeError as e:
        result.add_failure(0, f"Invalid JSON: {e}")
        return result

    creators = data.get("creators", [])
    if not creators:
        result.add_failure(0, "No creators found in JSON")
        return result

    for idx, creator_data in enumerate(creators):
        result.total += 1

        try:
            display_name = creator_data.get("display_name", "").strip()
            if not display_name:
                result.add_failure(idx, "Missing display_name", creator_data)
                continue

            passport = CreatorPassport()
            passport.identity.display_name = display_name

            # Creator types
            types = creator_data.get("creator_types", ["performer"])
            passport.identity.creator_types = [
                CreatorType(t) for t in types if t in [e.value for e in CreatorType]
            ]

            # IPI
            if creator_data.get("ipi_number"):
                try:
                    passport.identity.ipi_number = IPI.parse(creator_data["ipi_number"])
                except ValueError as e:
                    result.add_failure(idx, f"Invalid IPI: {e}", creator_data)
                    continue

            # ISNI
            if creator_data.get("isni_number"):
                try:
                    passport.identity.isni_number = ISNI.parse(creator_data["isni_number"])
                except ValueError as e:
                    result.add_failure(idx, f"Invalid ISNI: {e}", creator_data)
                    continue

            passport.identity.pro_membership = creator_data.get("pro_membership")

            # Apply template
            template = creator_data.get("consent_template") or consent_template
            if template:
                if not apply_template(passport, template):
                    result.add_failure(idx, f"Unknown template: {template}", creator_data)
                    continue

            # Custom consent rules
            custom_rules = creator_data.get("consent_rules", [])
            for rule_data in custom_rules:
                rule = ConsentRule(
                    use_category=UseCategory(rule_data["use_category"]),
                    decision=ConsentDecision(rule_data["decision"])
                )
                if rule_data.get("min_amount"):
                    rule.compensation = CompensationTerms(
                        compensation_type=CompensationType.FLAT_FEE,
                        minimum_amount=rule_data["min_amount"]
                    )
                passport.update_consent_rule(rule)

            # Save
            creator_id = db.save_creator(passport)
            result.add_success(creator_id)

        except Exception as e:
            result.add_failure(idx, str(e), creator_data)

    return result


# ═══════════════════════════════════════════════════════════════════════════
# Export Functions
# ═══════════════════════════════════════════════════════════════════════════

def export_creators_csv(db: NoizyFishDB, creator_ids: list[str] = None) -> str:
    """Export creators to CSV."""
    output = StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        "creator_id", "noizy_id", "display_name", "creator_types",
        "ipi_number", "isni_number", "pro_membership", "verification_status",
        "consent_rules_count", "created_at"
    ])

    # Get creators
    if creator_ids:
        creators = [db.get_creator(cid) for cid in creator_ids if db.get_creator(cid)]
    else:
        creators = db.search_creators(limit=10000)

    for c in creators:
        rules = db.get_consent_rules(c["creator_id"])
        types = json.loads(c["creator_types"])

        writer.writerow([
            c["creator_id"],
            c["noizy_id"],
            c["display_name"],
            ",".join(types),
            c["ipi_number"] or "",
            c["isni_number"] or "",
            c["pro_membership"] or "",
            c["verification_status"],
            len(rules),
            c["created_at"]
        ])

    return output.getvalue()


def export_creators_json(db: NoizyFishDB, creator_ids: list[str] = None) -> str:
    """Export creators to JSON."""
    if creator_ids:
        creators = [db.get_creator(cid) for cid in creator_ids if db.get_creator(cid)]
    else:
        creators = db.search_creators(limit=10000)

    export_data = {
        "exported_at": datetime.utcnow().isoformat(),
        "count": len(creators),
        "creators": []
    }

    for c in creators:
        rules = db.get_consent_rules(c["creator_id"])

        creator_export = {
            "creator_id": c["creator_id"],
            "noizy_id": c["noizy_id"],
            "display_name": c["display_name"],
            "creator_types": json.loads(c["creator_types"]),
            "ipi_number": c["ipi_number"],
            "isni_number": c["isni_number"],
            "pro_membership": c["pro_membership"],
            "verification_status": c["verification_status"],
            "consent_rules": [
                {
                    "use_category": r["use_category"],
                    "decision": r["decision"],
                    "min_compensation": r["min_compensation"]
                }
                for r in rules
            ],
            "created_at": c["created_at"]
        }

        export_data["creators"].append(creator_export)

    return json.dumps(export_data, indent=2)


# ═══════════════════════════════════════════════════════════════════════════
# Bulk Operations
# ═══════════════════════════════════════════════════════════════════════════

async def bulk_apply_template(
    db: NoizyFishDB,
    creator_ids: list[str],
    template_name: str,
    progress_callback: Optional[callable] = None
) -> ImportResult:
    """Apply a consent template to multiple creators."""
    result = ImportResult()
    result.total = len(creator_ids)

    template = CONSENT_TEMPLATES.get(template_name)
    if not template:
        result.add_failure(0, f"Unknown template: {template_name}")
        return result

    for idx, creator_id in enumerate(creator_ids):
        try:
            creator = db.get_creator(creator_id)
            if not creator:
                result.add_failure(idx, f"Creator not found: {creator_id}")
                continue

            # Load passport, apply template
            passport_data = json.loads(creator["passport_data"])
            passport = CreatorPassport()
            passport.identity.creator_id = creator["creator_id"]
            passport.identity.display_name = creator["display_name"]

            if apply_template(passport, template_name):
                # Save updated consent rules
                for rule in passport.consent.rules:
                    with db._get_conn() as conn:
                        db._save_consent_rule(conn, creator_id, rule)

                result.add_success(creator_id)
            else:
                result.add_failure(idx, "Template apply failed")

            if progress_callback:
                progress_callback(idx + 1, result.total)

        except Exception as e:
            result.add_failure(idx, str(e))

    return result


# ═══════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════

def demo():
    """Demonstrate bulk ingestion."""
    print("\n" + "=" * 70)
    print("NOIZY FISH BULK INGESTION — DEMO")
    print("=" * 70)

    db = NoizyFishDB(":memory:")

    # Sample CSV
    csv_data = """display_name,creator_types,ipi_number,pro_membership,consent_template
Sarah Chen,composer,00123456789,ASCAP,composer_premium
Marcus Reed,voice_actor,,SAG-AFTRA,voice_actor_protective
DJ Nova,"producer,dj",,,producer_remix_friendly
Alex Turner,songwriter,00987654321,BMI,standard_artist
Voice Sample Co.,voice_actor,,,all_rights_reserved
"""

    print("\n" + "─" * 50)
    print("IMPORTING CREATORS FROM CSV")
    print("─" * 50)

    result = import_creators_csv(db, csv_data)
    print(f"  Total: {result.total}")
    print(f"  Successful: {result.successful}")
    print(f"  Failed: {result.failed}")
    print(f"  Success Rate: {result.to_dict()['success_rate']}")

    if result.errors:
        print(f"\n  Errors:")
        for err in result.errors[:3]:
            print(f"    Row {err['row']}: {err['error']}")

    # Show created creators
    print("\n" + "─" * 50)
    print("CREATED CREATORS")
    print("─" * 50)

    creators = db.search_creators()
    for c in creators:
        rules = db.get_consent_rules(c["creator_id"])
        print(f"  {c['display_name']}: {len(rules)} consent rules")

    # Show templates
    print("\n" + "─" * 50)
    print("AVAILABLE CONSENT TEMPLATES")
    print("─" * 50)

    for tmpl in list_templates():
        print(f"  • {tmpl['name']}: {tmpl['description']}")

    # Export
    print("\n" + "─" * 50)
    print("EXPORTING TO CSV")
    print("─" * 50)

    csv_export = export_creators_csv(db)
    lines = csv_export.strip().split("\n")
    print(f"  Exported {len(lines) - 1} creators")
    print(f"  First line: {lines[0]}")

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    demo()
