"""
Providence Chain
================
Immutable record of all consent decisions and licensing transactions.

Every decision, every inquiry, every approval or decline —
recorded forever with cryptographic proof.

This is the audit trail that proves creator rights were respected.
"""

import hashlib
import json
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional, Any
from pathlib import Path
import asyncio


@dataclass
class ProvidenceRecord:
    """A single record in the providence chain."""
    record_id: str
    record_type: str  # licensing_inquiry, consent_update, violation, etc.
    timestamp: str
    data: dict
    previous_hash: str
    record_hash: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ChainState:
    """Current state of the providence chain."""
    chain_id: str
    created_at: str
    last_updated: str
    record_count: int
    latest_hash: str
    records: list[ProvidenceRecord] = field(default_factory=list)


class ProvidenceChain:
    """
    The immutable providence chain for consent records.

    Features:
    - Cryptographic hashing of all records
    - Chain integrity verification
    - Gabriel MCP integration for persistence
    - Full audit trail

    Each record includes:
    - What happened
    - When it happened
    - Hash of previous record (chain integrity)
    - Hash of this record (tamper detection)
    """

    def __init__(self, gabriel_mcp_client=None, storage_path: Optional[Path] = None):
        self.gabriel = gabriel_mcp_client
        self.storage_path = storage_path or Path.home() / ".noizy" / "providence"
        self.storage_path.mkdir(parents=True, exist_ok=True)

        self.chain_file = self.storage_path / "chain.json"
        self.state = self._load_or_create_chain()

    def _load_or_create_chain(self) -> ChainState:
        """Load existing chain or create new one."""
        if self.chain_file.exists():
            try:
                data = json.loads(self.chain_file.read_text())
                records = [ProvidenceRecord(**r) for r in data.get("records", [])]
                return ChainState(
                    chain_id=data["chain_id"],
                    created_at=data["created_at"],
                    last_updated=data["last_updated"],
                    record_count=data["record_count"],
                    latest_hash=data["latest_hash"],
                    records=records
                )
            except Exception as e:
                print(f"Warning: Could not load chain: {e}")

        # Create genesis block
        genesis = self._create_genesis_record()
        state = ChainState(
            chain_id=self._generate_id(),
            created_at=datetime.utcnow().isoformat(),
            last_updated=datetime.utcnow().isoformat(),
            record_count=1,
            latest_hash=genesis.record_hash,
            records=[genesis]
        )
        self._save_chain(state)
        return state

    def _create_genesis_record(self) -> ProvidenceRecord:
        """Create the first record in the chain."""
        record_id = self._generate_id()
        timestamp = datetime.utcnow().isoformat()
        data = {
            "type": "genesis",
            "message": "NOIZY.ai Providence Chain initialized",
            "version": "1.0.0"
        }

        record_hash = self._hash_record(record_id, "genesis", timestamp, data, "0")

        return ProvidenceRecord(
            record_id=record_id,
            record_type="genesis",
            timestamp=timestamp,
            data=data,
            previous_hash="0",
            record_hash=record_hash
        )

    async def add_record(self, data: dict) -> str:
        """
        Add a new record to the chain.
        Returns the record hash.
        """
        record_id = self._generate_id()
        timestamp = datetime.utcnow().isoformat()
        record_type = data.get("type", "unknown")
        previous_hash = self.state.latest_hash

        record_hash = self._hash_record(
            record_id, record_type, timestamp, data, previous_hash
        )

        record = ProvidenceRecord(
            record_id=record_id,
            record_type=record_type,
            timestamp=timestamp,
            data=data,
            previous_hash=previous_hash,
            record_hash=record_hash
        )

        # Add to chain
        self.state.records.append(record)
        self.state.record_count += 1
        self.state.latest_hash = record_hash
        self.state.last_updated = timestamp

        # Persist
        self._save_chain(self.state)

        # Sync to Gabriel MCP if available
        if self.gabriel:
            await self._sync_to_gabriel(record)

        return record_hash

    async def verify_chain(self) -> tuple[bool, list[str]]:
        """
        Verify the integrity of the entire chain.
        Returns (is_valid, list of issues).
        """
        issues = []

        if not self.state.records:
            issues.append("Chain is empty")
            return False, issues

        # Check genesis
        genesis = self.state.records[0]
        if genesis.previous_hash != "0":
            issues.append("Genesis block has invalid previous hash")

        # Verify each record
        for i, record in enumerate(self.state.records):
            # Verify hash
            expected_hash = self._hash_record(
                record.record_id,
                record.record_type,
                record.timestamp,
                record.data,
                record.previous_hash
            )

            if record.record_hash != expected_hash:
                issues.append(f"Record {i} ({record.record_id}): Hash mismatch")

            # Verify chain linkage
            if i > 0:
                prev_record = self.state.records[i - 1]
                if record.previous_hash != prev_record.record_hash:
                    issues.append(f"Record {i}: Chain broken (wrong previous hash)")

        return len(issues) == 0, issues

    def get_record(self, record_hash: str) -> Optional[ProvidenceRecord]:
        """Get a record by its hash."""
        for record in self.state.records:
            if record.record_hash == record_hash:
                return record
        return None

    def get_records_by_type(self, record_type: str) -> list[ProvidenceRecord]:
        """Get all records of a specific type."""
        return [r for r in self.state.records if r.record_type == record_type]

    def get_records_for_work(self, work_id: str) -> list[ProvidenceRecord]:
        """Get all records related to a specific work."""
        results = []
        for record in self.state.records:
            if record.data.get("work_id") == work_id:
                results.append(record)
            # Check nested data
            if "inquiry" in record.data:
                if record.data["inquiry"].get("work_id") == work_id:
                    results.append(record)
        return results

    def _hash_record(
        self,
        record_id: str,
        record_type: str,
        timestamp: str,
        data: dict,
        previous_hash: str
    ) -> str:
        """Generate cryptographic hash for a record."""
        content = json.dumps({
            "record_id": record_id,
            "record_type": record_type,
            "timestamp": timestamp,
            "data": data,
            "previous_hash": previous_hash
        }, sort_keys=True)

        return hashlib.sha256(content.encode()).hexdigest()

    def _generate_id(self) -> str:
        """Generate a unique record ID."""
        import uuid
        return str(uuid.uuid4())

    def _save_chain(self, state: ChainState):
        """Persist chain to disk."""
        data = {
            "chain_id": state.chain_id,
            "created_at": state.created_at,
            "last_updated": state.last_updated,
            "record_count": state.record_count,
            "latest_hash": state.latest_hash,
            "records": [r.to_dict() for r in state.records]
        }
        self.chain_file.write_text(json.dumps(data, indent=2))

    async def _sync_to_gabriel(self, record: ProvidenceRecord):
        """Sync record to Gabriel MCP for distributed storage."""
        if self.gabriel:
            await self.gabriel.call_tool(
                "providence_sync",
                {"record": record.to_dict()}
            )

    def export_chain(self, format: str = "json") -> str:
        """Export the entire chain."""
        if format == "json":
            return json.dumps({
                "chain_id": self.state.chain_id,
                "exported_at": datetime.utcnow().isoformat(),
                "record_count": self.state.record_count,
                "records": [r.to_dict() for r in self.state.records]
            }, indent=2)

        elif format == "markdown":
            md = f"# Providence Chain Export\n\n"
            md += f"**Chain ID:** `{self.state.chain_id}`\n"
            md += f"**Records:** {self.state.record_count}\n"
            md += f"**Created:** {self.state.created_at}\n\n"
            md += "---\n\n"

            for record in self.state.records:
                md += f"## Record: `{record.record_hash[:16]}...`\n\n"
                md += f"- **Type:** {record.record_type}\n"
                md += f"- **Time:** {record.timestamp}\n"
                md += f"- **Previous:** `{record.previous_hash[:16]}...`\n\n"
                md += "```json\n"
                md += json.dumps(record.data, indent=2)
                md += "\n```\n\n---\n\n"

            return md

        return ""


class ProvidenceViewer:
    """View and explore providence records."""

    def __init__(self, chain: ProvidenceChain):
        self.chain = chain

    def get_licensing_history(self, work_id: str) -> list[dict]:
        """Get complete licensing history for a work."""
        records = self.chain.get_records_for_work(work_id)
        history = []

        for record in records:
            if record.record_type == "licensing_inquiry":
                decision = record.data.get("decision", {})
                history.append({
                    "date": record.timestamp,
                    "type": "inquiry",
                    "requestor": record.data.get("inquiry", {}).get("requestor_name"),
                    "use_type": record.data.get("inquiry", {}).get("use_type"),
                    "status": decision.get("status"),
                    "approved": decision.get("approved"),
                    "hash": record.record_hash
                })

        return sorted(history, key=lambda x: x["date"], reverse=True)

    def generate_audit_report(self, work_id: str) -> str:
        """Generate an audit report for a work."""
        records = self.chain.get_records_for_work(work_id)

        report = f"# Audit Report\n\n"
        report += f"**Work ID:** {work_id}\n"
        report += f"**Generated:** {datetime.utcnow().isoformat()}\n"
        report += f"**Total Records:** {len(records)}\n\n"
        report += "---\n\n"

        for record in records:
            report += f"### {record.record_type.upper()}\n"
            report += f"**Time:** {record.timestamp}\n"
            report += f"**Hash:** `{record.record_hash}`\n\n"

            if record.record_type == "licensing_inquiry":
                inquiry = record.data.get("inquiry", {})
                decision = record.data.get("decision", {})

                report += f"**Requestor:** {inquiry.get('requestor_name')}\n"
                report += f"**Use Type:** {inquiry.get('use_type')}\n"
                report += f"**Decision:** {'APPROVED' if decision.get('approved') else 'DECLINED'}\n\n"

            report += "---\n\n"

        return report
