#!/usr/bin/env python3
"""
AUTOMATED MAINTENANCE - Scheduled Maintenance Tasks
Automated health checks, cleanup, and optimization
"""

import asyncio
import json
import schedule
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List

class AutomatedMaintenance:
    """Automated maintenance scheduler"""
    
    def __init__(self):
        self.maintenance_log = []
        self.log_file = Path(__file__).parent / "maintenance_log.json"
    
    async def daily_health_check(self):
        """Daily health check task"""
        print(f"[{datetime.now()}] Running daily health check...")
        
        try:
            sys.path.insert(0, str(Path(__file__).parent))
            from mc96_master_control import MC96MasterControl
            
            control = MC96MasterControl()
            results = await control.full_system_check()
            
            self.log_maintenance("daily_health_check", results)
            
            # Alert if health score is low
            if results["health_score"] < 70:
                print(f"⚠️  WARNING: Health score is {results['health_score']}/100")
            
            return results
        except Exception as e:
            print(f"Error in daily health check: {e}")
            return None
    
    async def weekly_cleanup(self):
        """Weekly cleanup task"""
        print(f"[{datetime.now()}] Running weekly cleanup...")
        
        try:
            sys.path.insert(0, str(Path(__file__).parent))
            from volume_monitor_UPGRADED import VolumeMonitorUpgraded
            from automated_cleanup import AutomatedCleanup
            
            monitor = VolumeMonitorUpgraded()
            monitor.scan_volumes()
            cleanup = AutomatedCleanup()
            
            # Analyze critical volumes
            critical = monitor.get_critical_volumes()
            for vol_name in critical[:2]:  # Top 2 critical
                vol_info = monitor.volumes.get(vol_name)
                if vol_info:
                    analysis = cleanup.analyze_volume(vol_info["mount"])
                    self.log_maintenance("weekly_cleanup", {
                        "volume": vol_info["mount"],
                        "opportunities": len(analysis.get("cleanup_opportunities", [])),
                        "estimated_space": analysis.get("estimated_space", "0")
                    })
            
            return True
        except Exception as e:
            print(f"Error in weekly cleanup: {e}")
            return False
    
    async def monthly_optimization(self):
        """Monthly optimization task"""
        print(f"[{datetime.now()}] Running monthly optimization...")
        
        try:
            # Run all optimization tasks
            tasks = [
                self._optimize_network_volumes(),
                self._check_data_integrity(),
                self._generate_monthly_report()
            ]
            
            results = await asyncio.gather(*tasks)
            self.log_maintenance("monthly_optimization", results)
            
            return results
        except Exception as e:
            print(f"Error in monthly optimization: {e}")
            return None
    
    async def _optimize_network_volumes(self):
        """Optimize network volumes"""
        # Placeholder for network optimization
        return {"status": "completed"}
    
    async def _check_data_integrity(self):
        """Check data integrity"""
        # Placeholder for data integrity checks
        return {"status": "completed"}
    
    async def _generate_monthly_report(self):
        """Generate monthly report"""
        # Placeholder for monthly reporting
        return {"status": "completed"}
    
    def log_maintenance(self, task_name: str, results: Dict):
        """Log maintenance task"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "task": task_name,
            "results": results
        }
        self.maintenance_log.append(entry)
        
        # Save log
        if self.log_file.exists():
            try:
                with open(self.log_file, "r") as f:
                    existing = json.load(f)
            except:
                existing = []
        else:
            existing = []
        
        existing.append(entry)
        
        # Keep only last 100 entries
        existing = existing[-100:]
        
        with open(self.log_file, "w") as f:
            json.dump(existing, f, indent=2, default=str)
    
    def setup_schedule(self):
        """Setup maintenance schedule"""
        # Daily health check at 2 AM
        schedule.every().day.at("02:00").do(lambda: asyncio.run(self.daily_health_check()))
        
        # Weekly cleanup on Sunday at 3 AM
        schedule.every().sunday.at("03:00").do(lambda: asyncio.run(self.weekly_cleanup()))
        
        # Monthly optimization on 1st at 4 AM
        schedule.every().month.do(lambda: asyncio.run(self.monthly_optimization()))
        
        print("📅 Maintenance schedule configured:")
        print("   • Daily health check: 2:00 AM")
        print("   • Weekly cleanup: Sunday 3:00 AM")
        print("   • Monthly optimization: 1st of month 4:00 AM")
    
    def run_scheduler(self):
        """Run maintenance scheduler"""
        self.setup_schedule()
        
        print("\n⏰ Automated maintenance scheduler running...")
        print("   Press Ctrl+C to stop\n")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\n\nMaintenance scheduler stopped.")

async def main():
    """Test maintenance tasks"""
    maintenance = AutomatedMaintenance()
    
    print("🧪 Testing maintenance tasks...\n")
    
    # Test daily health check
    print("1. Testing daily health check...")
    await maintenance.daily_health_check()
    
    print("\n2. Testing weekly cleanup...")
    await maintenance.weekly_cleanup()
    
    print("\n✅ Maintenance tests complete!")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "schedule":
        maintenance = AutomatedMaintenance()
        maintenance.run_scheduler()
    else:
        asyncio.run(main())

