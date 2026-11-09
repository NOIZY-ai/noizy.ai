#!/usr/bin/env python3
"""
MC96ECOUNIVERSE MASTER CONTROL CENTER
Unified command center for all MC96 operations
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import subprocess

class MC96MasterControl:
    """Master control center for MC96ECOUNIVERSE"""
    
    def __init__(self):
        self.modules = {
            "monitor": self._load_module("volume_monitor_UPGRADED", "VolumeMonitorUpgraded"),
            "network": self._load_module("network_volume_optimizer", "NetworkVolumeOptimizer"),
            "cleanup": self._load_module("automated_cleanup", "AutomatedCleanup"),
            "hpomen": self._load_module("hp_omen_integration", "HPOMENIntegration"),
        }
    
    def _load_module(self, module_name: str, class_name: str):
        """Dynamically load module"""
        try:
            sys.path.insert(0, str(Path(__file__).parent))
            module = __import__(module_name)
            return getattr(module, class_name)()
        except Exception as e:
            print(f"Warning: Could not load {module_name}: {e}")
            return None
    
    async def full_system_check(self) -> Dict:
        """Run complete system health check"""
        print("🔍 RUNNING FULL SYSTEM CHECK...\n")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "volumes": await self._check_volumes(),
            "network": await self._check_network(),
            "hpomen": await self._check_hpomen(),
            "cleanup": await self._check_cleanup_opportunities(),
            "performance": await self._check_performance(),
            "health_score": 0
        }
        
        # Calculate health score
        results["health_score"] = self._calculate_health_score(results)
        
        return results
    
    async def _check_volumes(self) -> Dict:
        """Check all volumes"""
        if not self.modules["monitor"]:
            return {"error": "Monitor not loaded"}
        
        volumes = await self.modules["monitor"].scan_volumes_async()
        # Get critical volumes from already scanned data
        critical = [
            name for name, info in volumes.items()
            if info.get('percent', 0) >= 95
        ]
        # Get network volumes from already scanned data
        network = {
            name: info for name, info in volumes.items()
            if info.get('is_network', False)
        }
        
        return {
            "total": len(volumes),
            "critical": len(critical),
            "network": len(network),
            "critical_volumes": critical,
            "status": "OK" if len(critical) == 0 else "WARNING"
        }
    
    async def _check_network(self) -> Dict:
        """Check network volumes"""
        if not self.modules["network"]:
            return {"error": "Network optimizer not loaded"}
        
        volumes = await self.modules["network"].detect_network_volumes()
        
        return {
            "volumes": len(volumes),
            "status": "OK" if len(volumes) > 0 else "ERROR",
            "network_volumes": volumes
        }
    
    async def _check_hpomen(self) -> Dict:
        """Check HP-OMEN connection"""
        if not self.modules["hpomen"]:
            return {"error": "HP-OMEN integration not loaded"}
        
        connected = await self.modules["hpomen"].check_connection()
        volumes = self.modules["hpomen"].get_network_volumes()
        
        return {
            "connected": connected,
            "volumes": len(volumes),
            "status": "CONNECTED" if connected else "DISCONNECTED"
        }
    
    async def _check_cleanup_opportunities(self) -> Dict:
        """Check cleanup opportunities"""
        if not self.modules["cleanup"]:
            return {"error": "Cleanup system not loaded"}
        
        # Check critical volumes for cleanup
        if self.modules["monitor"]:
            # Use async method when in async context
            critical = await self.modules["monitor"].get_critical_volumes_async()
            if critical and self.modules["monitor"].volumes:
                opportunities = []
                for vol_name in critical[:2]:  # Check first 2 critical
                    vol_info = self.modules["monitor"].volumes.get(vol_name)
                    if vol_info:
                        analysis = self.modules["cleanup"].analyze_volume(vol_info["mount"])
                        if "cleanup_opportunities" in analysis:
                            opportunities.append({
                                "volume": vol_info["mount"],
                                "opportunities": len(analysis["cleanup_opportunities"]),
                                "estimated_space": analysis.get("estimated_space", "0")
                            })
                return {
                    "opportunities": len(opportunities),
                    "details": opportunities
                }
        
        return {"opportunities": 0}
    
    async def _check_performance(self) -> Dict:
        """Check system performance"""
        # Check CPU, memory, disk I/O
        try:
            # Simple performance check
            start = datetime.now()
            test_file = Path("/tmp/mc96_perf_test")
            test_file.write_text("performance test")
            test_file.unlink()
            elapsed = (datetime.now() - start).total_seconds()
            
            return {
                "disk_io_ms": round(elapsed * 1000, 2),
                "status": "OK" if elapsed < 0.1 else "SLOW"
            }
        except:
            return {"status": "ERROR"}
    
    def _calculate_health_score(self, results: Dict) -> int:
        """Calculate overall health score (0-100)"""
        score = 100
        
        # Deduct for critical volumes
        volumes = results.get("volumes", {})
        critical_count = volumes.get("critical", 0)
        score -= (critical_count * 20)  # -20 per critical volume
        
        # Deduct for network issues
        network = results.get("network", {})
        if network.get("status") == "ERROR":
            score -= 15
        
        # Deduct for HP-OMEN disconnection
        hpomen = results.get("hpomen", {})
        if not hpomen.get("connected"):
            score -= 10
        
        # Deduct for slow performance
        performance = results.get("performance", {})
        if performance.get("status") == "SLOW":
            score -= 5
        
        return max(0, min(100, score))
    
    def print_status_dashboard(self, results: Dict):
        """Print beautiful status dashboard"""
        print("\n" + "="*70)
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║         MC96ECOUNIVERSE MASTER CONTROL CENTER                ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"\n📅 Status: {results['timestamp']}")
        print(f"💚 Health Score: {results['health_score']}/100")
        
        # Volumes
        volumes = results.get("volumes", {})
        print(f"\n📁 VOLUMES:")
        print(f"   Total: {volumes.get('total', 0)}")
        print(f"   Critical: {volumes.get('critical', 0)}")
        print(f"   Network: {volumes.get('network', 0)}")
        if volumes.get('critical_volumes'):
            print(f"   ⚠️  Critical: {', '.join(volumes['critical_volumes'][:3])}")
        
        # Network
        network = results.get("network", {})
        print(f"\n🌐 NETWORK:")
        print(f"   Volumes: {network.get('volumes', 0)}")
        print(f"   Status: {network.get('status', 'UNKNOWN')}")
        
        # HP-OMEN
        hpomen = results.get("hpomen", {})
        print(f"\n🖥️  HP-OMEN:")
        print(f"   Connected: {'✅' if hpomen.get('connected') else '❌'}")
        print(f"   Volumes: {hpomen.get('volumes', 0)}")
        
        # Cleanup
        cleanup = results.get("cleanup", {})
        print(f"\n🧹 CLEANUP:")
        print(f"   Opportunities: {cleanup.get('opportunities', 0)}")
        if cleanup.get('details'):
            for detail in cleanup['details'][:2]:
                print(f"   • {detail['volume']}: {detail['estimated_space']} available")
        
        # Performance
        perf = results.get("performance", {})
        print(f"\n⚡ PERFORMANCE:")
        print(f"   Disk I/O: {perf.get('disk_io_ms', 'N/A')}ms")
        print(f"   Status: {perf.get('status', 'UNKNOWN')}")
        
        print("\n" + "="*70 + "\n")

async def main():
    """Main control center"""
    control = MC96MasterControl()
    
    # Run full system check
    results = await control.full_system_check()
    
    # Print dashboard
    control.print_status_dashboard(results)
    
    # Save results
    results_path = Path(__file__).parent / "master_control_status.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"📊 Status saved to: {results_path}")

if __name__ == "__main__":
    asyncio.run(main())

