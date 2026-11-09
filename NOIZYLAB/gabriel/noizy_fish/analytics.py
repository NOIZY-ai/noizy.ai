"""
NOIZY Fish — Analytics & Reporting
====================================

Comprehensive analytics for:
- Inquiry patterns (approved/denied rates)
- Revenue tracking
- Geographic distribution
- Use category trends
- Creator activity
- Platform performance

Provides:
- Real-time metrics
- Historical reports
- Trend analysis
- Export to various formats
"""

import json
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
import sqlite3

from .registry import NoizyFishDB


# ═══════════════════════════════════════════════════════════════════════════
# Metrics
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class InquiryMetrics:
    """Metrics for licensing inquiries."""
    total: int = 0
    approved: int = 0
    denied: int = 0
    pending: int = 0
    approval_rate: float = 0.0
    denial_rate: float = 0.0
    avg_offer: float = 0.0
    total_value: float = 0.0

    def calculate_rates(self):
        if self.total > 0:
            self.approval_rate = self.approved / self.total * 100
            self.denial_rate = self.denied / self.total * 100


@dataclass
class RevenueMetrics:
    """Revenue metrics."""
    total_licensed: float = 0.0
    total_denied_value: float = 0.0  # Value of rejected offers
    avg_deal_size: float = 0.0
    by_category: dict = field(default_factory=dict)
    by_territory: dict = field(default_factory=dict)


@dataclass
class CreatorMetrics:
    """Metrics for a single creator."""
    creator_id: str = ""
    display_name: str = ""
    inquiries_received: int = 0
    inquiries_approved: int = 0
    inquiries_denied: int = 0
    total_licensed_value: float = 0.0
    total_denied_value: float = 0.0
    most_requested_category: str = ""
    consent_rules_count: int = 0


@dataclass
class PlatformMetrics:
    """Platform-wide metrics."""
    total_creators: int = 0
    total_works: int = 0
    total_inquiries: int = 0
    total_licenses: int = 0
    inquiry_metrics: InquiryMetrics = field(default_factory=InquiryMetrics)
    revenue_metrics: RevenueMetrics = field(default_factory=RevenueMetrics)
    top_creators: list = field(default_factory=list)
    top_categories: list = field(default_factory=list)
    verification_breakdown: dict = field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════════════════
# Analytics Engine
# ═══════════════════════════════════════════════════════════════════════════

class AnalyticsEngine:
    """
    Analytics engine for NOIZY Fish.
    Computes metrics from the registry database.
    """

    def __init__(self, db: NoizyFishDB):
        self.db = db

    # ─────────────────────────────────────────────────────────────────────────
    # Inquiry Analytics
    # ─────────────────────────────────────────────────────────────────────────

    def get_inquiry_metrics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        creator_id: Optional[str] = None
    ) -> InquiryMetrics:
        """Get inquiry metrics for a time period."""
        metrics = InquiryMetrics()

        with self.db._get_conn() as conn:
            sql = "SELECT decision, offered_amount FROM inquiries WHERE 1=1"
            params = []

            if start_date:
                sql += " AND created_at >= ?"
                params.append(start_date.isoformat())

            if end_date:
                sql += " AND created_at <= ?"
                params.append(end_date.isoformat())

            if creator_id:
                sql += " AND creator_id = ?"
                params.append(creator_id)

            rows = conn.execute(sql, params).fetchall()

            total_offers = 0
            for row in rows:
                metrics.total += 1
                decision = row["decision"]
                offer = row["offered_amount"] or 0

                if decision in ["allowed", "allowed_terms"]:
                    metrics.approved += 1
                    metrics.total_value += offer
                elif decision == "denied":
                    metrics.denied += 1
                else:
                    metrics.pending += 1

                total_offers += offer

            if metrics.total > 0:
                metrics.avg_offer = total_offers / metrics.total

            metrics.calculate_rates()

        return metrics

    def get_inquiry_trends(
        self,
        days: int = 30,
        granularity: str = "day"  # day, week, month
    ) -> list[dict]:
        """Get inquiry trends over time."""
        trends = []

        with self.db._get_conn() as conn:
            # SQLite date grouping
            if granularity == "day":
                date_format = "%Y-%m-%d"
            elif granularity == "week":
                date_format = "%Y-W%W"
            else:
                date_format = "%Y-%m"

            sql = f"""
                SELECT
                    strftime('{date_format}', created_at) as period,
                    decision,
                    COUNT(*) as count,
                    SUM(COALESCE(offered_amount, 0)) as total_value
                FROM inquiries
                WHERE created_at >= date('now', '-{days} days')
                GROUP BY period, decision
                ORDER BY period
            """

            rows = conn.execute(sql).fetchall()

            # Aggregate by period
            by_period = defaultdict(lambda: {"approved": 0, "denied": 0, "pending": 0, "value": 0})

            for row in rows:
                period = row["period"]
                decision = row["decision"]
                count = row["count"]
                value = row["total_value"] or 0

                if decision in ["allowed", "allowed_terms"]:
                    by_period[period]["approved"] += count
                    by_period[period]["value"] += value
                elif decision == "denied":
                    by_period[period]["denied"] += count
                else:
                    by_period[period]["pending"] += count

            for period, data in sorted(by_period.items()):
                total = data["approved"] + data["denied"] + data["pending"]
                trends.append({
                    "period": period,
                    "total": total,
                    "approved": data["approved"],
                    "denied": data["denied"],
                    "pending": data["pending"],
                    "approval_rate": data["approved"] / total * 100 if total > 0 else 0,
                    "total_value": data["value"]
                })

        return trends

    # ─────────────────────────────────────────────────────────────────────────
    # Category Analytics
    # ─────────────────────────────────────────────────────────────────────────

    def get_category_breakdown(self) -> list[dict]:
        """Get inquiry breakdown by use category."""
        categories = []

        with self.db._get_conn() as conn:
            sql = """
                SELECT
                    use_category,
                    decision,
                    COUNT(*) as count,
                    SUM(COALESCE(offered_amount, 0)) as total_value,
                    AVG(COALESCE(offered_amount, 0)) as avg_value
                FROM inquiries
                GROUP BY use_category, decision
                ORDER BY use_category
            """

            rows = conn.execute(sql).fetchall()

            by_category = defaultdict(lambda: {
                "total": 0, "approved": 0, "denied": 0,
                "total_value": 0, "avg_value": 0
            })

            for row in rows:
                cat = row["use_category"]
                decision = row["decision"]
                count = row["count"]
                value = row["total_value"] or 0
                avg = row["avg_value"] or 0

                by_category[cat]["total"] += count

                if decision in ["allowed", "allowed_terms"]:
                    by_category[cat]["approved"] += count
                    by_category[cat]["total_value"] += value
                elif decision == "denied":
                    by_category[cat]["denied"] += count

            for cat, data in sorted(by_category.items(), key=lambda x: -x[1]["total"]):
                categories.append({
                    "category": cat,
                    "total": data["total"],
                    "approved": data["approved"],
                    "denied": data["denied"],
                    "approval_rate": data["approved"] / data["total"] * 100 if data["total"] > 0 else 0,
                    "total_value": data["total_value"]
                })

        return categories

    def get_ai_consent_stats(self) -> dict:
        """Get specific stats on AI-related consent decisions."""
        ai_categories = ["ai_training", "ai_voice_clone", "ai_generation", "ai_style_transfer"]

        with self.db._get_conn() as conn:
            sql = """
                SELECT
                    use_category,
                    decision,
                    COUNT(*) as count,
                    SUM(COALESCE(offered_amount, 0)) as total_value
                FROM inquiries
                WHERE use_category IN ({})
                GROUP BY use_category, decision
            """.format(",".join(f"'{c}'" for c in ai_categories))

            rows = conn.execute(sql).fetchall()

            stats = {
                "total_ai_inquiries": 0,
                "ai_approved": 0,
                "ai_denied": 0,
                "ai_approval_rate": 0,
                "total_ai_value_offered": 0,
                "total_ai_value_denied": 0,
                "by_type": {}
            }

            for row in rows:
                cat = row["use_category"]
                decision = row["decision"]
                count = row["count"]
                value = row["total_value"] or 0

                stats["total_ai_inquiries"] += count

                if cat not in stats["by_type"]:
                    stats["by_type"][cat] = {"approved": 0, "denied": 0, "value_offered": 0}

                if decision in ["allowed", "allowed_terms"]:
                    stats["ai_approved"] += count
                    stats["by_type"][cat]["approved"] += count
                elif decision == "denied":
                    stats["ai_denied"] += count
                    stats["total_ai_value_denied"] += value
                    stats["by_type"][cat]["denied"] += count

                stats["total_ai_value_offered"] += value
                stats["by_type"][cat]["value_offered"] += value

            if stats["total_ai_inquiries"] > 0:
                stats["ai_approval_rate"] = stats["ai_approved"] / stats["total_ai_inquiries"] * 100

        return stats

    # ─────────────────────────────────────────────────────────────────────────
    # Creator Analytics
    # ─────────────────────────────────────────────────────────────────────────

    def get_creator_metrics(self, creator_id: str) -> CreatorMetrics:
        """Get metrics for a specific creator."""
        metrics = CreatorMetrics(creator_id=creator_id)

        with self.db._get_conn() as conn:
            # Get creator info
            creator = conn.execute(
                "SELECT display_name FROM creators WHERE creator_id = ?",
                (creator_id,)
            ).fetchone()

            if creator:
                metrics.display_name = creator["display_name"]

            # Get consent rules count
            rules = conn.execute(
                "SELECT COUNT(*) FROM consent_rules WHERE creator_id = ?",
                (creator_id,)
            ).fetchone()
            metrics.consent_rules_count = rules[0]

            # Get inquiry stats
            sql = """
                SELECT
                    use_category,
                    decision,
                    COUNT(*) as count,
                    SUM(COALESCE(offered_amount, 0)) as total_value
                FROM inquiries
                WHERE creator_id = ?
                GROUP BY use_category, decision
            """

            rows = conn.execute(sql, (creator_id,)).fetchall()

            category_counts = defaultdict(int)

            for row in rows:
                cat = row["use_category"]
                decision = row["decision"]
                count = row["count"]
                value = row["total_value"] or 0

                metrics.inquiries_received += count
                category_counts[cat] += count

                if decision in ["allowed", "allowed_terms"]:
                    metrics.inquiries_approved += count
                    metrics.total_licensed_value += value
                elif decision == "denied":
                    metrics.inquiries_denied += count
                    metrics.total_denied_value += value

            if category_counts:
                metrics.most_requested_category = max(category_counts, key=category_counts.get)

        return metrics

    def get_top_creators(self, limit: int = 10, metric: str = "inquiries") -> list[dict]:
        """Get top creators by various metrics."""
        creators = []

        with self.db._get_conn() as conn:
            if metric == "inquiries":
                sql = """
                    SELECT
                        c.creator_id,
                        c.display_name,
                        COUNT(i.inquiry_id) as count,
                        SUM(CASE WHEN i.decision IN ('allowed', 'allowed_terms') THEN 1 ELSE 0 END) as approved
                    FROM creators c
                    LEFT JOIN inquiries i ON c.creator_id = i.creator_id
                    GROUP BY c.creator_id
                    ORDER BY count DESC
                    LIMIT ?
                """
            elif metric == "value":
                sql = """
                    SELECT
                        c.creator_id,
                        c.display_name,
                        SUM(COALESCE(i.offered_amount, 0)) as count,
                        COUNT(i.inquiry_id) as approved
                    FROM creators c
                    LEFT JOIN inquiries i ON c.creator_id = i.creator_id
                    WHERE i.decision IN ('allowed', 'allowed_terms')
                    GROUP BY c.creator_id
                    ORDER BY count DESC
                    LIMIT ?
                """
            else:
                sql = """
                    SELECT
                        c.creator_id,
                        c.display_name,
                        COUNT(w.work_id) as count,
                        0 as approved
                    FROM creators c
                    LEFT JOIN works w ON c.creator_id = w.creator_id
                    GROUP BY c.creator_id
                    ORDER BY count DESC
                    LIMIT ?
                """

            rows = conn.execute(sql, (limit,)).fetchall()

            for row in rows:
                creators.append({
                    "creator_id": row["creator_id"],
                    "display_name": row["display_name"],
                    "value": row["count"],
                    "secondary": row["approved"]
                })

        return creators

    # ─────────────────────────────────────────────────────────────────────────
    # Platform Analytics
    # ─────────────────────────────────────────────────────────────────────────

    def get_platform_metrics(self) -> PlatformMetrics:
        """Get comprehensive platform metrics."""
        metrics = PlatformMetrics()

        # Get basic stats
        stats = self.db.get_stats()
        metrics.total_creators = stats["creators"]
        metrics.total_works = stats["works"]
        metrics.total_inquiries = stats["inquiries"]
        metrics.total_licenses = stats["licenses"]

        # Get inquiry metrics
        metrics.inquiry_metrics = self.get_inquiry_metrics()

        # Get top creators
        metrics.top_creators = self.get_top_creators(5)

        # Get top categories
        categories = self.get_category_breakdown()
        metrics.top_categories = categories[:5]

        # Get verification breakdown
        with self.db._get_conn() as conn:
            rows = conn.execute("""
                SELECT verification_status, COUNT(*) as count
                FROM creators
                GROUP BY verification_status
            """).fetchall()

            for row in rows:
                metrics.verification_breakdown[row["verification_status"]] = row["count"]

        return metrics

    # ─────────────────────────────────────────────────────────────────────────
    # Reports
    # ─────────────────────────────────────────────────────────────────────────

    def generate_report(
        self,
        report_type: str = "summary",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        format: str = "dict"
    ) -> dict:
        """Generate a comprehensive report."""
        if not end_date:
            end_date = datetime.utcnow()
        if not start_date:
            start_date = end_date - timedelta(days=30)

        report = {
            "report_type": report_type,
            "generated_at": datetime.utcnow().isoformat(),
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            }
        }

        if report_type == "summary":
            report["platform"] = {
                "total_creators": self.db.get_stats()["creators"],
                "total_works": self.db.get_stats()["works"],
                "total_inquiries": self.db.get_stats()["inquiries"]
            }
            report["inquiry_metrics"] = self.get_inquiry_metrics(start_date, end_date).__dict__
            report["top_categories"] = self.get_category_breakdown()[:5]
            report["ai_stats"] = self.get_ai_consent_stats()

        elif report_type == "trends":
            report["daily_trends"] = self.get_inquiry_trends(30, "day")
            report["weekly_trends"] = self.get_inquiry_trends(90, "week")

        elif report_type == "ai_focus":
            report["ai_stats"] = self.get_ai_consent_stats()
            report["message"] = "AI consent is being actively protected by creators"

        return report

    def export_report_markdown(self, report: dict) -> str:
        """Export report as markdown."""
        md = f"""# NOIZY Fish Analytics Report

**Generated:** {report['generated_at']}
**Period:** {report['period']['start'][:10]} to {report['period']['end'][:10]}

---

## Platform Overview

| Metric | Value |
|--------|-------|
"""
        if "platform" in report:
            for key, value in report["platform"].items():
                md += f"| {key.replace('_', ' ').title()} | {value:,} |\n"

        if "inquiry_metrics" in report:
            im = report["inquiry_metrics"]
            md += f"""
## Inquiry Metrics

| Metric | Value |
|--------|-------|
| Total Inquiries | {im['total']:,} |
| Approved | {im['approved']:,} ({im['approval_rate']:.1f}%) |
| Denied | {im['denied']:,} ({im['denial_rate']:.1f}%) |
| Average Offer | ${im['avg_offer']:,.2f} |
| Total Licensed Value | ${im['total_value']:,.2f} |
"""

        if "ai_stats" in report:
            ai = report["ai_stats"]
            md += f"""
## AI Consent Stats

| Metric | Value |
|--------|-------|
| Total AI Inquiries | {ai['total_ai_inquiries']:,} |
| AI Approved | {ai['ai_approved']:,} |
| AI Denied | {ai['ai_denied']:,} |
| AI Approval Rate | {ai['ai_approval_rate']:.1f}% |
| Total AI Value Denied | ${ai['total_ai_value_denied']:,.2f} |

**Creators are actively protecting their work from unauthorized AI use.**
"""

        if "top_categories" in report:
            md += "\n## Top Categories\n\n| Category | Total | Approved | Rate |\n|----------|-------|----------|------|\n"
            for cat in report["top_categories"]:
                md += f"| {cat['category']} | {cat['total']} | {cat['approved']} | {cat['approval_rate']:.1f}% |\n"

        md += "\n---\n*NOIZY Fish — Creator consent as the foundation*\n"

        return md


# ═══════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════

def demo():
    """Demonstrate analytics."""
    print("\n" + "=" * 70)
    print("NOIZY FISH ANALYTICS — DEMO")
    print("=" * 70)

    # Use existing database if available
    from pathlib import Path
    db_path = "noizy_fish.db"

    if not Path(db_path).exists():
        print("\n⚠️  No database found. Run dashboard demo first:")
        print("   python -m gabriel.noizy_fish.dashboard --demo")
        return

    db = NoizyFishDB(db_path)
    analytics = AnalyticsEngine(db)

    # Platform metrics
    print("\n" + "─" * 50)
    print("PLATFORM METRICS")
    print("─" * 50)

    platform = analytics.get_platform_metrics()
    print(f"  Creators: {platform.total_creators}")
    print(f"  Works: {platform.total_works}")
    print(f"  Inquiries: {platform.total_inquiries}")

    # Inquiry metrics
    print("\n" + "─" * 50)
    print("INQUIRY METRICS")
    print("─" * 50)

    im = platform.inquiry_metrics
    print(f"  Total: {im.total}")
    print(f"  Approved: {im.approved} ({im.approval_rate:.1f}%)")
    print(f"  Denied: {im.denied} ({im.denial_rate:.1f}%)")
    print(f"  Avg Offer: ${im.avg_offer:,.2f}")

    # Category breakdown
    print("\n" + "─" * 50)
    print("CATEGORY BREAKDOWN")
    print("─" * 50)

    categories = analytics.get_category_breakdown()
    for cat in categories[:5]:
        print(f"  {cat['category']}: {cat['total']} inquiries ({cat['approval_rate']:.0f}% approved)")

    # AI stats
    print("\n" + "─" * 50)
    print("AI CONSENT STATS")
    print("─" * 50)

    ai = analytics.get_ai_consent_stats()
    print(f"  Total AI Inquiries: {ai['total_ai_inquiries']}")
    print(f"  AI Approved: {ai['ai_approved']} ({ai['ai_approval_rate']:.1f}%)")
    print(f"  AI Denied: {ai['ai_denied']}")
    print(f"  Value Denied: ${ai['total_ai_value_denied']:,.2f}")

    # Generate report
    print("\n" + "─" * 50)
    print("GENERATING REPORT")
    print("─" * 50)

    report = analytics.generate_report("summary")
    md = analytics.export_report_markdown(report)
    print(f"  Report generated: {len(md)} characters")
    print(f"  Preview:\n{md[:500]}...")

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    demo()
