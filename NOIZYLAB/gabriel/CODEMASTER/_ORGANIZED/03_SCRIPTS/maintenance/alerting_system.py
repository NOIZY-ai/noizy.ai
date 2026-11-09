#!/usr/bin/env python3
"""
ALERTING SYSTEM - Smart Notifications
Email, Slack, and system alerts for critical events
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class AlertingSystem:
    """Smart alerting system for MC96ECOUNIVERSE"""
    
    def __init__(self):
        self.alert_log = []
        self.log_file = Path(__file__).parent / "alert_log.json"
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load alerting configuration"""
        config_file = Path(__file__).parent / "alert_config.json"
        if config_file.exists():
            try:
                with open(config_file, "r") as f:
                    return json.load(f)
            except:
                pass
        
        # Default config
        return {
            "slack_webhook": None,
            "email_enabled": False,
            "critical_threshold": 95,
            "warning_threshold": 85,
            "alert_on_disconnect": True
        }
    
    def send_alert(self, level: str, title: str, message: str, data: Optional[Dict] = None):
        """Send alert (level: critical, warning, info)"""
        alert = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "title": title,
            "message": message,
            "data": data or {}
        }
        
        self.alert_log.append(alert)
        self._save_alert_log()
        
        # Send notifications based on level
        if level == "critical":
            self._send_critical_alert(alert)
        elif level == "warning":
            self._send_warning_alert(alert)
        
        # System notification (macOS)
        self._send_system_notification(level, title, message)
    
    def _send_system_notification(self, level: str, title: str, message: str):
        """Send macOS system notification"""
        try:
            icon = "🚨" if level == "critical" else "⚠️" if level == "warning" else "ℹ️"
            subprocess.run([
                "osascript", "-e",
                f'display notification "{message}" with title "{icon} {title}"'
            ], capture_output=True, timeout=5)
        except:
            pass
    
    def _send_critical_alert(self, alert: Dict):
        """Send critical alert notifications"""
        # System notification already sent
        # Could add Slack, email, etc. here
        print(f"🚨 CRITICAL: {alert['title']} - {alert['message']}")
    
    def _send_warning_alert(self, alert: Dict):
        """Send warning alert notifications"""
        print(f"⚠️  WARNING: {alert['title']} - {alert['message']}")
    
    def _save_alert_log(self):
        """Save alert log"""
        # Keep only last 100 alerts
        recent = self.alert_log[-100:]
        with open(self.log_file, "w") as f:
            json.dump(recent, f, indent=2)
    
    async def check_and_alert(self, system_status: Dict):
        """Check system status and send alerts if needed"""
        # Check critical volumes
        volumes = system_status.get("volumes", {})
        critical = volumes.get("critical_volumes", [])
        
        if critical:
            self.send_alert(
                "critical",
                "Critical Volume Alert",
                f"{len(critical)} volumes at critical capacity: {', '.join(critical[:3])}",
                {"critical_volumes": critical}
            )
        
        # Check HP-OMEN connection
        hpomen = system_status.get("hpomen", {})
        if not hpomen.get("connected"):
            self.send_alert(
                "critical",
                "HP-OMEN Disconnected",
                "HP-OMEN system is not connected",
                {"hpomen": hpomen}
            )
        
        # Check health score
        health_score = system_status.get("health_score", 100)
        if health_score < 50:
            self.send_alert(
                "critical",
                "Low Health Score",
                f"System health score is {health_score}/100",
                {"health_score": health_score}
            )
        elif health_score < 70:
            self.send_alert(
                "warning",
                "Degraded Health Score",
                f"System health score is {health_score}/100",
                {"health_score": health_score}
            )
    
    def get_recent_alerts(self, limit: int = 10) -> List[Dict]:
        """Get recent alerts"""
        return self.alert_log[-limit:]
    
    def generate_alert_report(self) -> str:
        """Generate alert report"""
        critical_count = sum(1 for a in self.alert_log if a["level"] == "critical")
        warning_count = sum(1 for a in self.alert_log if a["level"] == "warning")
        
        report = []
        report.append("╔══════════════════════════════════════════════════════════════╗")
        report.append("║              ALERT SYSTEM REPORT                            ║")
        report.append("╚══════════════════════════════════════════════════════════════╝")
        report.append(f"\n📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.append(f"🚨 Critical Alerts: {critical_count}")
        report.append(f"⚠️  Warning Alerts: {warning_count}")
        report.append(f"📊 Total Alerts: {len(self.alert_log)}\n")
        
        if self.alert_log:
            report.append("RECENT ALERTS:")
            report.append("─" * 70)
            for alert in self.alert_log[-10:]:
                icon = "🚨" if alert["level"] == "critical" else "⚠️"
                report.append(f"\n{icon} [{alert['timestamp'][:19]}] {alert['title']}")
                report.append(f"   {alert['message']}")
        
        return "\n".join(report)

async def main():
    """Test alerting system"""
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from mc96_master_control import MC96MasterControl
    
    alerting = AlertingSystem()
    control = MC96MasterControl()
    
    print("🔔 Testing alerting system...\n")
    
    # Get system status
    status = await control.full_system_check()
    
    # Check and send alerts
    await alerting.check_and_alert(status)
    
    # Generate report
    report = alerting.generate_alert_report()
    print("\n" + report)
    
    # Save report
    report_path = Path(__file__).parent / "alert_report.md"
    with open(report_path, "w") as f:
        f.write(report)
    print(f"\n📊 Report saved to: {report_path}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())


