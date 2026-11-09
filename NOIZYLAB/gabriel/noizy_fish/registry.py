"""
NOIZY Fish — Persistent Registry
=================================

SQLite-backed storage for:
- Creator Passports
- Consent Registries
- Providence Manifests
- Licenses
- Transaction Log

Designed for millions of creators with fast consent lookups.
"""

import json
import sqlite3
from contextlib import contextmanager
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Optional
import hashlib

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
from .standards import IPI, ISNI, NoizyID, ContributorRole


class NoizyFishDB:
    """
    SQLite database for NOIZY Fish registry.
    Handles all persistence operations.
    """

    def __init__(self, db_path: str = "noizy_fish.db"):
        self.db_path = db_path
        self._conn = None
        # For :memory: databases, keep a persistent connection
        if db_path == ":memory:":
            self._conn = sqlite3.connect(":memory:")
            self._conn.row_factory = sqlite3.Row
        self._init_db()

    @contextmanager
    def _get_conn(self):
        """Context manager for database connections."""
        # Use persistent connection for in-memory databases
        if self._conn:
            try:
                yield self._conn
                self._conn.commit()
            except Exception:
                self._conn.rollback()
                raise
        else:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            try:
                yield conn
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                conn.close()

    def _init_db(self):
        """Initialize database schema."""
        with self._get_conn() as conn:
            conn.executescript("""
                -- Creator Passports
                CREATE TABLE IF NOT EXISTS creators (
                    creator_id TEXT PRIMARY KEY,
                    noizy_id TEXT UNIQUE NOT NULL,
                    display_name TEXT NOT NULL,
                    legal_name_hash TEXT,
                    creator_types TEXT NOT NULL,  -- JSON array
                    primary_role TEXT,
                    ipi_number TEXT,
                    isni_number TEXT,
                    pro_membership TEXT,
                    pro_member_id TEXT,
                    email_hash TEXT,
                    verification_status TEXT DEFAULT 'unverified',
                    public_key TEXT,
                    passport_data TEXT NOT NULL,  -- Full JSON
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_creators_noizy_id ON creators(noizy_id);
                CREATE INDEX IF NOT EXISTS idx_creators_ipi ON creators(ipi_number);
                CREATE INDEX IF NOT EXISTS idx_creators_display_name ON creators(display_name);

                -- Consent Rules (denormalized for fast lookups)
                CREATE TABLE IF NOT EXISTS consent_rules (
                    rule_id TEXT PRIMARY KEY,
                    creator_id TEXT NOT NULL,
                    use_category TEXT NOT NULL,
                    decision TEXT NOT NULL,
                    allowed_territories TEXT,  -- JSON array
                    excluded_territories TEXT,  -- JSON array
                    excluded_parties TEXT,  -- JSON array
                    excluded_contexts TEXT,  -- JSON array
                    min_compensation REAL,
                    compensation_type TEXT,
                    rule_data TEXT NOT NULL,  -- Full JSON
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY (creator_id) REFERENCES creators(creator_id)
                );

                CREATE INDEX IF NOT EXISTS idx_consent_creator ON consent_rules(creator_id);
                CREATE INDEX IF NOT EXISTS idx_consent_use ON consent_rules(use_category);
                CREATE INDEX IF NOT EXISTS idx_consent_lookup ON consent_rules(creator_id, use_category);

                -- Works (recordings, compositions, voices)
                CREATE TABLE IF NOT EXISTS works (
                    work_id TEXT PRIMARY KEY,
                    noizy_work_id TEXT UNIQUE NOT NULL,
                    creator_id TEXT NOT NULL,
                    work_type TEXT NOT NULL,  -- recording, composition, voice
                    title TEXT NOT NULL,
                    isrc TEXT,
                    iswc TEXT,
                    format TEXT,
                    manifest_data TEXT,  -- C2PA manifest JSON
                    consent_registry_id TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY (creator_id) REFERENCES creators(creator_id)
                );

                CREATE INDEX IF NOT EXISTS idx_works_creator ON works(creator_id);
                CREATE INDEX IF NOT EXISTS idx_works_isrc ON works(isrc);
                CREATE INDEX IF NOT EXISTS idx_works_iswc ON works(iswc);

                -- Licenses
                CREATE TABLE IF NOT EXISTS licenses (
                    license_id TEXT PRIMARY KEY,
                    work_id TEXT NOT NULL,
                    licensor_id TEXT NOT NULL,
                    licensee_name TEXT NOT NULL,
                    licensee_email TEXT,
                    licensee_company TEXT,
                    use_type TEXT NOT NULL,
                    territory TEXT DEFAULT 'WW',
                    status TEXT DEFAULT 'pending',
                    fee_type TEXT,
                    fee_amount REAL,
                    license_data TEXT NOT NULL,  -- Full JSON
                    created_at TEXT NOT NULL,
                    activated_at TEXT,
                    expires_at TEXT,
                    FOREIGN KEY (work_id) REFERENCES works(work_id),
                    FOREIGN KEY (licensor_id) REFERENCES creators(creator_id)
                );

                CREATE INDEX IF NOT EXISTS idx_licenses_work ON licenses(work_id);
                CREATE INDEX IF NOT EXISTS idx_licenses_licensor ON licenses(licensor_id);
                CREATE INDEX IF NOT EXISTS idx_licenses_status ON licenses(status);

                -- Transaction Log (append-only)
                CREATE TABLE IF NOT EXISTS transaction_log (
                    entry_id TEXT PRIMARY KEY,
                    entry_index INTEGER NOT NULL,
                    transaction_type TEXT NOT NULL,
                    entity_id TEXT,
                    entity_type TEXT,
                    details TEXT NOT NULL,  -- JSON
                    previous_hash TEXT NOT NULL,
                    entry_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_txlog_entity ON transaction_log(entity_id, entity_type);
                CREATE INDEX IF NOT EXISTS idx_txlog_type ON transaction_log(transaction_type);

                -- Audit Trail (for consent changes)
                CREATE TABLE IF NOT EXISTS audit_trail (
                    audit_id TEXT PRIMARY KEY,
                    creator_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    details TEXT NOT NULL,  -- JSON
                    entry_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (creator_id) REFERENCES creators(creator_id)
                );

                CREATE INDEX IF NOT EXISTS idx_audit_creator ON audit_trail(creator_id);

                -- Licensing Inquiries (for tracking requests)
                CREATE TABLE IF NOT EXISTS inquiries (
                    inquiry_id TEXT PRIMARY KEY,
                    work_id TEXT,
                    creator_id TEXT NOT NULL,
                    requestor_name TEXT NOT NULL,
                    requestor_email TEXT,
                    use_category TEXT NOT NULL,
                    territory TEXT DEFAULT 'WW',
                    context TEXT,
                    offered_amount REAL,
                    decision TEXT,
                    decision_reasons TEXT,  -- JSON array
                    responded_at TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (creator_id) REFERENCES creators(creator_id)
                );

                CREATE INDEX IF NOT EXISTS idx_inquiries_creator ON inquiries(creator_id);
                CREATE INDEX IF NOT EXISTS idx_inquiries_decision ON inquiries(decision);
            """)

    # ═══════════════════════════════════════════════════════════════════
    # Creator Operations
    # ═══════════════════════════════════════════════════════════════════

    def save_creator(self, passport: CreatorPassport) -> str:
        """Save or update a creator passport."""
        now = datetime.utcnow().isoformat()

        # Serialize passport
        passport_json = json.dumps(passport.to_dict(), default=str)

        with self._get_conn() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO creators (
                    creator_id, noizy_id, display_name, creator_types,
                    primary_role, ipi_number, isni_number, pro_membership,
                    pro_member_id, email_hash, verification_status,
                    public_key, passport_data, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                passport.identity.creator_id,
                str(passport.identity.noizy_id),
                passport.identity.display_name,
                json.dumps([t.value for t in passport.identity.creator_types]),
                passport.identity.primary_role.value if passport.identity.primary_role else None,
                str(passport.identity.ipi_number) if passport.identity.ipi_number else None,
                str(passport.identity.isni_number) if passport.identity.isni_number else None,
                passport.identity.pro_membership,
                passport.identity.pro_member_id,
                passport.identity.email_hash,
                passport.identity.verification_status.value,
                passport.identity.public_key,
                passport_json,
                passport.created_at.isoformat(),
                now
            ))

            # Save consent rules
            for rule in passport.consent.rules:
                self._save_consent_rule(conn, passport.identity.creator_id, rule)

        return passport.identity.creator_id

    def _save_consent_rule(self, conn, creator_id: str, rule: ConsentRule):
        """Save a consent rule."""
        now = datetime.utcnow().isoformat()

        rule_data = {
            "rule_id": rule.rule_id,
            "use_category": rule.use_category.value,
            "decision": rule.decision.value,
            "allowed_territories": rule.allowed_territories,
            "excluded_territories": rule.excluded_territories,
            "excluded_parties": rule.excluded_parties,
            "excluded_contexts": rule.excluded_contexts,
            "duration_limit": rule.duration_limit,
            "requires_credit": rule.requires_credit,
            "credit_format": rule.credit_format,
            "additional_terms": rule.additional_terms
        }

        if rule.compensation:
            rule_data["compensation"] = {
                "type": rule.compensation.compensation_type.value,
                "minimum": rule.compensation.minimum_amount,
                "preferred": rule.compensation.preferred_amount,
                "percentage": rule.compensation.percentage_rate,
                "per_use": rule.compensation.per_use_rate,
                "currency": rule.compensation.currency
            }

        conn.execute("""
            INSERT OR REPLACE INTO consent_rules (
                rule_id, creator_id, use_category, decision,
                allowed_territories, excluded_territories,
                excluded_parties, excluded_contexts,
                min_compensation, compensation_type,
                rule_data, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            rule.rule_id,
            creator_id,
            rule.use_category.value,
            rule.decision.value,
            json.dumps(rule.allowed_territories),
            json.dumps(rule.excluded_territories),
            json.dumps(rule.excluded_parties),
            json.dumps(rule.excluded_contexts),
            rule.compensation.minimum_amount if rule.compensation else None,
            rule.compensation.compensation_type.value if rule.compensation else None,
            json.dumps(rule_data),
            rule.created_at.isoformat(),
            now
        ))

    def get_creator(self, creator_id: str) -> Optional[dict]:
        """Get a creator by ID."""
        with self._get_conn() as conn:
            row = conn.execute(
                "SELECT * FROM creators WHERE creator_id = ?",
                (creator_id,)
            ).fetchone()

            if row:
                return dict(row)
        return None

    def get_creator_by_noizy_id(self, noizy_id: str) -> Optional[dict]:
        """Get a creator by NOIZY ID."""
        with self._get_conn() as conn:
            row = conn.execute(
                "SELECT * FROM creators WHERE noizy_id = ?",
                (noizy_id,)
            ).fetchone()

            if row:
                return dict(row)
        return None

    def search_creators(
        self,
        query: Optional[str] = None,
        creator_type: Optional[str] = None,
        limit: int = 50
    ) -> list[dict]:
        """Search for creators."""
        with self._get_conn() as conn:
            sql = "SELECT * FROM creators WHERE 1=1"
            params = []

            if query:
                sql += " AND (display_name LIKE ? OR noizy_id LIKE ?)"
                params.extend([f"%{query}%", f"%{query}%"])

            if creator_type:
                sql += " AND creator_types LIKE ?"
                params.append(f"%{creator_type}%")

            sql += f" ORDER BY updated_at DESC LIMIT {limit}"

            rows = conn.execute(sql, params).fetchall()
            return [dict(row) for row in rows]

    # ═══════════════════════════════════════════════════════════════════
    # Consent Lookup (Fast Path)
    # ═══════════════════════════════════════════════════════════════════

    def check_consent(
        self,
        creator_id: str,
        use_category: str,
        requestor: Optional[str] = None,
        context: Optional[str] = None,
        territory: str = "WW",
        offered_amount: Optional[float] = None
    ) -> dict:
        """
        Fast consent check — the core query for licensing inquiries.
        Returns decision and reasons.
        """
        with self._get_conn() as conn:
            # Get the rule for this use category
            row = conn.execute("""
                SELECT * FROM consent_rules
                WHERE creator_id = ? AND use_category = ?
            """, (creator_id, use_category)).fetchone()

            if not row:
                # No specific rule — get creator's default
                creator = conn.execute(
                    "SELECT passport_data FROM creators WHERE creator_id = ?",
                    (creator_id,)
                ).fetchone()

                if not creator:
                    return {
                        "decision": "error",
                        "reasons": ["Creator not found"]
                    }

                passport_data = json.loads(creator["passport_data"])
                default = passport_data.get("consent", {}).get("default_decision", "requires_approval")

                return {
                    "decision": default,
                    "reasons": [f"No rule for {use_category}, using default"]
                }

            # Parse rule data
            rule_data = json.loads(row["rule_data"])
            decision = row["decision"]
            reasons = []

            # Check excluded parties
            excluded_parties = json.loads(row["excluded_parties"] or "[]")
            if requestor and excluded_parties:
                for excluded in excluded_parties:
                    if excluded.lower() in requestor.lower():
                        return {
                            "decision": "denied",
                            "reasons": [f"Requestor matches excluded party: {excluded}"]
                        }

            # Check excluded contexts
            excluded_contexts = json.loads(row["excluded_contexts"] or "[]")
            if context and excluded_contexts:
                for excluded in excluded_contexts:
                    if excluded.lower() in context.lower():
                        return {
                            "decision": "denied",
                            "reasons": [f"Context matches exclusion: {excluded}"]
                        }

            # Check territory
            allowed_territories = json.loads(row["allowed_territories"] or '["WW"]')
            excluded_territories = json.loads(row["excluded_territories"] or "[]")

            if territory in excluded_territories:
                return {
                    "decision": "denied",
                    "reasons": [f"Territory {territory} is excluded"]
                }

            if territory not in allowed_territories and "WW" not in allowed_territories:
                return {
                    "decision": "denied",
                    "reasons": [f"Territory {territory} not in allowed list"]
                }

            # Check compensation
            min_comp = row["min_compensation"]
            if min_comp and offered_amount:
                if offered_amount < min_comp:
                    return {
                        "decision": "denied",
                        "reasons": [f"Offer ${offered_amount} below minimum ${min_comp}"]
                    }
                reasons.append(f"Offer ${offered_amount} meets minimum ${min_comp}")

            reasons.append(f"Rule decision: {decision}")

            return {
                "decision": decision,
                "reasons": reasons,
                "rule_id": row["rule_id"],
                "compensation": {
                    "minimum": min_comp,
                    "type": row["compensation_type"]
                } if min_comp else None
            }

    def get_consent_rules(self, creator_id: str) -> list[dict]:
        """Get all consent rules for a creator."""
        with self._get_conn() as conn:
            rows = conn.execute(
                "SELECT * FROM consent_rules WHERE creator_id = ? ORDER BY use_category",
                (creator_id,)
            ).fetchall()
            return [dict(row) for row in rows]

    # ═══════════════════════════════════════════════════════════════════
    # Work Operations
    # ═══════════════════════════════════════════════════════════════════

    def save_work(
        self,
        work_id: str,
        noizy_work_id: str,
        creator_id: str,
        work_type: str,
        title: str,
        isrc: Optional[str] = None,
        iswc: Optional[str] = None,
        format: Optional[str] = None,
        manifest_data: Optional[dict] = None
    ) -> str:
        """Save a work (recording, composition, voice asset)."""
        now = datetime.utcnow().isoformat()

        with self._get_conn() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO works (
                    work_id, noizy_work_id, creator_id, work_type,
                    title, isrc, iswc, format, manifest_data,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                work_id,
                noizy_work_id,
                creator_id,
                work_type,
                title,
                isrc,
                iswc,
                format,
                json.dumps(manifest_data) if manifest_data else None,
                now,
                now
            ))

        return work_id

    def get_work(self, work_id: str) -> Optional[dict]:
        """Get a work by ID."""
        with self._get_conn() as conn:
            row = conn.execute(
                "SELECT * FROM works WHERE work_id = ? OR noizy_work_id = ?",
                (work_id, work_id)
            ).fetchone()

            if row:
                return dict(row)
        return None

    def get_works_by_creator(self, creator_id: str) -> list[dict]:
        """Get all works by a creator."""
        with self._get_conn() as conn:
            rows = conn.execute(
                "SELECT * FROM works WHERE creator_id = ? ORDER BY created_at DESC",
                (creator_id,)
            ).fetchall()
            return [dict(row) for row in rows]

    # ═══════════════════════════════════════════════════════════════════
    # Inquiry Logging
    # ═══════════════════════════════════════════════════════════════════

    def log_inquiry(
        self,
        creator_id: str,
        requestor_name: str,
        use_category: str,
        decision: str,
        reasons: list[str],
        work_id: Optional[str] = None,
        requestor_email: Optional[str] = None,
        territory: str = "WW",
        context: Optional[str] = None,
        offered_amount: Optional[float] = None
    ) -> str:
        """Log a licensing inquiry and decision."""
        from uuid import uuid4
        inquiry_id = str(uuid4())
        now = datetime.utcnow().isoformat()

        with self._get_conn() as conn:
            conn.execute("""
                INSERT INTO inquiries (
                    inquiry_id, work_id, creator_id, requestor_name,
                    requestor_email, use_category, territory, context,
                    offered_amount, decision, decision_reasons,
                    responded_at, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                inquiry_id,
                work_id,
                creator_id,
                requestor_name,
                requestor_email,
                use_category,
                territory,
                context,
                offered_amount,
                decision,
                json.dumps(reasons),
                now,
                now
            ))

        return inquiry_id

    def get_inquiries(
        self,
        creator_id: Optional[str] = None,
        decision: Optional[str] = None,
        limit: int = 100
    ) -> list[dict]:
        """Get inquiries with optional filters."""
        with self._get_conn() as conn:
            sql = "SELECT * FROM inquiries WHERE 1=1"
            params = []

            if creator_id:
                sql += " AND creator_id = ?"
                params.append(creator_id)

            if decision:
                sql += " AND decision = ?"
                params.append(decision)

            sql += f" ORDER BY created_at DESC LIMIT {limit}"

            rows = conn.execute(sql, params).fetchall()
            return [dict(row) for row in rows]

    # ═══════════════════════════════════════════════════════════════════
    # Transaction Log
    # ═══════════════════════════════════════════════════════════════════

    def log_transaction(
        self,
        transaction_type: str,
        details: dict,
        entity_id: Optional[str] = None,
        entity_type: Optional[str] = None
    ) -> str:
        """Add entry to immutable transaction log."""
        from uuid import uuid4

        with self._get_conn() as conn:
            # Get previous hash
            last = conn.execute(
                "SELECT entry_hash, entry_index FROM transaction_log ORDER BY entry_index DESC LIMIT 1"
            ).fetchone()

            if last:
                previous_hash = last["entry_hash"]
                entry_index = last["entry_index"] + 1
            else:
                previous_hash = "0"
                entry_index = 0

            entry_id = str(uuid4())
            now = datetime.utcnow().isoformat()

            # Calculate hash
            hash_data = {
                "entry_id": entry_id,
                "entry_index": entry_index,
                "transaction_type": transaction_type,
                "details": details,
                "previous_hash": previous_hash,
                "created_at": now
            }
            entry_hash = hashlib.sha256(
                json.dumps(hash_data, sort_keys=True).encode()
            ).hexdigest()

            conn.execute("""
                INSERT INTO transaction_log (
                    entry_id, entry_index, transaction_type,
                    entity_id, entity_type, details,
                    previous_hash, entry_hash, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry_id,
                entry_index,
                transaction_type,
                entity_id,
                entity_type,
                json.dumps(details),
                previous_hash,
                entry_hash,
                now
            ))

        return entry_id

    def verify_transaction_log(self) -> tuple[bool, list[str]]:
        """Verify integrity of transaction log."""
        issues = []

        with self._get_conn() as conn:
            rows = conn.execute(
                "SELECT * FROM transaction_log ORDER BY entry_index"
            ).fetchall()

            for i, row in enumerate(rows):
                # Verify chain
                if i > 0:
                    if row["previous_hash"] != rows[i-1]["entry_hash"]:
                        issues.append(f"Entry {i}: Chain broken")

                # Verify hash
                hash_data = {
                    "entry_id": row["entry_id"],
                    "entry_index": row["entry_index"],
                    "transaction_type": row["transaction_type"],
                    "details": json.loads(row["details"]),
                    "previous_hash": row["previous_hash"],
                    "created_at": row["created_at"]
                }
                expected_hash = hashlib.sha256(
                    json.dumps(hash_data, sort_keys=True).encode()
                ).hexdigest()

                if row["entry_hash"] != expected_hash:
                    issues.append(f"Entry {i}: Hash mismatch")

        return len(issues) == 0, issues

    # ═══════════════════════════════════════════════════════════════════
    # Stats
    # ═══════════════════════════════════════════════════════════════════

    def get_stats(self) -> dict:
        """Get registry statistics."""
        with self._get_conn() as conn:
            creators = conn.execute("SELECT COUNT(*) FROM creators").fetchone()[0]
            works = conn.execute("SELECT COUNT(*) FROM works").fetchone()[0]
            rules = conn.execute("SELECT COUNT(*) FROM consent_rules").fetchone()[0]
            licenses = conn.execute("SELECT COUNT(*) FROM licenses").fetchone()[0]
            inquiries = conn.execute("SELECT COUNT(*) FROM inquiries").fetchone()[0]
            txlog = conn.execute("SELECT COUNT(*) FROM transaction_log").fetchone()[0]

            # Decisions breakdown
            decisions = conn.execute("""
                SELECT decision, COUNT(*) as count
                FROM inquiries
                GROUP BY decision
            """).fetchall()

            return {
                "creators": creators,
                "works": works,
                "consent_rules": rules,
                "licenses": licenses,
                "inquiries": inquiries,
                "transaction_log_entries": txlog,
                "decisions": {row["decision"]: row["count"] for row in decisions}
            }
