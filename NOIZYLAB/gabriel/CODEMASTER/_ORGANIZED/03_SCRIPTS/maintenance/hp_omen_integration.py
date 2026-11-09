#!/usr/bin/env python3
"""
HP-OMEN INTEGRATION - Unified Monitoring & Control
Bridge m2ultra & HP-OMEN Gabriel systems
"""

import subprocess
import json
import socket
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import asyncio

class HPOMENIntegration:
    """HP-OMEN system integration"""
    
    HP_OMEN_IP = "10.0.0.160"
    HP_OMEN_NAME = "HP-OMEN"
    
    def __init__(self):
        self.network_volumes = []
        self.connection_status = False
        
    async def check_connection(self) -> bool:
        """Check HP-OMEN connectivity"""
        try:
            # Ping HP-OMEN
            proc = await asyncio.create_subprocess_exec(
                "ping", "-c", "1", "-t", "2", self.HP_OMEN_IP,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )
            await proc.wait()
            self.connection_status = proc.returncode == 0
            return self.connection_status
        except:
            self.connection_status = False
            return False
    
    def get_network_volumes(self) -> List[Dict]:
        """Get all HP-OMEN network volumes"""
        volumes = []
        try:
            result = subprocess.run(
                ["df", "-h"],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            for line in result.stdout.split('\n'):
                if self.HP_OMEN_IP in line or 'rsp@RSP' in line:
                    parts = line.split()
                    if len(parts) >= 6:
                        mount = ' '.join(parts[5:])
                        volumes.append({
                            "device": parts[0],
                            "mount": mount,
                            "size": parts[1],
                            "used": parts[2],
                            "available": parts[3],
                            "usage": parts[4],
                            "server": "HP-OMEN (RSP)",
                            "type": "SMB"
                        })
        except Exception as e:
            print(f"Error getting network volumes: {e}")
        
        self.network_volumes = volumes
        return volumes
    
    async def test_smb_performance(self, mount: str) -> Dict:
        """Test SMB volume performance"""
        try:
            test_file = Path(mount) / ".hp_omen_test"
            
            # Write test
            start = datetime.now()
            with open(test_file, 'w') as f:
                f.write("hp_omen_performance_test")
            write_time = (datetime.now() - start).total_seconds()
            
            # Read test
            start = datetime.now()
            with open(test_file, 'r') as f:
                f.read()
            read_time = (datetime.now() - start).total_seconds()
            
            # Cleanup
            test_file.unlink()
            
            return {
                "mount": mount,
                "write_latency_ms": round(write_time * 1000, 2),
                "read_latency_ms": round(read_time * 1000, 2),
                "status": "OK" if write_time < 0.5 and read_time < 0.5 else "SLOW"
            }
        except Exception as e:
            return {
                "mount": mount,
                "error": str(e),
                "status": "ERROR"
            }
    
    def generate_integration_report(self) -> str:
        """Generate HP-OMEN integration report"""
        report = []
        report.append("╔══════════════════════════════════════════════════════════════╗")
        report.append("║           HP-OMEN INTEGRATION REPORT                         ║")
        report.append("╚══════════════════════════════════════════════════════════════╝")
        report.append(f"\n📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        report.append(f"🖥️  HP-OMEN System: {self.HP_OMEN_NAME}")
        report.append(f"🌐 IP Address: {self.HP_OMEN_IP}")
        report.append(f"📡 Connection Status: {'✅ CONNECTED' if self.connection_status else '❌ DISCONNECTED'}\n")
        
        report.append(f"📁 Network Volumes: {len(self.network_volumes)}\n")
        
        if self.network_volumes:
            report.append("VOLUMES:")
            report.append("─" * 70)
            for vol in self.network_volumes:
                report.append(f"  • {vol['mount']}")
                report.append(f"    Usage: {vol['usage']}")
                report.append(f"    Available: {vol['available']}")
                report.append(f"    Server: {vol['server']}")
                report.append("")
        
        return "\n".join(report)

async def main():
    """Main integration function"""
    integration = HPOMENIntegration()
    
    print("🖥️  Checking HP-OMEN connection...")
    connected = await integration.check_connection()
    print(f"   {'✅ Connected' if connected else '❌ Not connected'}")
    
    print("\n📁 Getting network volumes...")
    volumes = integration.get_network_volumes()
    print(f"   Found {len(volumes)} HP-OMEN volumes")
    
    if volumes:
        print("\n⚡ Testing SMB performance...")
        for vol in volumes[:3]:  # Test first 3
            perf = await integration.test_smb_performance(vol['mount'])
            print(f"   {vol['mount']}: Write {perf.get('write_latency_ms', 'N/A')}ms, Read {perf.get('read_latency_ms', 'N/A')}ms")
    
    report = integration.generate_integration_report()
    print("\n" + report)
    
    # Save report
    report_path = Path(__file__).parent / "hp_omen_integration_report.md"
    with open(report_path, "w") as f:
        f.write(report)
    print(f"\n📊 Report saved to: {report_path}")

if __name__ == "__main__":
    asyncio.run(main())

