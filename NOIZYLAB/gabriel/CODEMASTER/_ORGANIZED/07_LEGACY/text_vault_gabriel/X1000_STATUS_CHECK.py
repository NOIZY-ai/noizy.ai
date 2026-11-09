#!/usr/bin/env python3
"""
🌟 X1000 COMPLETE SYSTEM STATUS 🌟
===================================
Real-time status checker for all X1000 systems
"""

import sys
from pathlib import Path
from datetime import datetime

def check_all_x1000_systems():
    """Check status of all X1000 systems"""
    
    gabriel_root = Path("/Users/rsp_ms/GABRIEL")
    
    systems = {
        "⚡ CORE X1000 SYSTEMS": [
            ("X1000_SUPREME_EXECUTOR.py", "Ultimate execution engine with quantum reliability"),
            ("X1000_SUPREME_INTEGRATION.py", "Quantum-level integration of all agents"),
            ("X1000_MASTER_LAUNCHER.py", "Unified launcher (created by integration)"),
        ],
        "🎯 X1000 SPECIALIZED SYSTEMS": [
            ("X1000_ENHANCED_FISHNET.py", "100+ pattern code scanner with AI"),
            ("X1000_OMNIDIRECTIONAL_PLUS.py", "14-direction quantum control"),
            ("X1000_CODE_VAC_ULTIMATE.py", "AI-powered code vacuum"),
            ("X1000_TERMINUS_ULTIMATE.py", "Quantum terminal with AI commands"),
            ("X1000_SCAN_ALL_DRIVES_ULTIMATE.py", "PERMANENT RULE drive scanner"),
            ("X1000_CODEBEAST_ULTIMATE.py", "Beast integration orchestrator"),
        ],
        "📦 ENHANCED ORIGINAL SYSTEMS": [
            ("autonomous_learning.py", "X1000 AI learning system"),
            ("GABRIEL_CODEMASTER.py", "Supreme orchestrator"),
            ("the_fishnet.py", "Original pattern scanner"),
            ("the_fishnet_universe.py", "Universe-wide scanner"),
            ("TERMINUS.py", "Shell-free terminal"),
            ("OMNIDIRECTIONAL.py", "Original 14-direction control"),
            ("SCAN_ALL_DRIVES.py", "PERMANENT RULE original"),
            ("CODE_VAC.py", "Original code vacuum"),
        ],
        "🔧 UTILITY SYSTEMS": [
            ("system_sound_manager.py", "macOS sound configuration"),
            ("spotify_crossfade.py", "Spotify settings"),
            ("TERMINUS_BRIDGE.py", "Termius API integration"),
            ("distribute_to_drives.py", "Drive distribution"),
            ("QUICK_DISTRIBUTE.py", "Quick distribution"),
            ("CHECK_DRIVES.py", "Drive monitor"),
            ("organize_12tb.py", "12TB organizer"),
        ],
        "🔗 INTEGRATION SYSTEMS": [
            ("SUPREME_INTEGRATION.py", "Original integration"),
            ("CODEBEAST_MEGA_INTEGRATION.py", "CODEBEAST integration"),
            ("INTEGRATE_CODEBEAST.py", "Basic CODEBEAST integration"),
        ]
    }
    
    print("=" * 80)
    print(" " * 25 + "🌟 X1000 SYSTEM STATUS 🌟")
    print("=" * 80)
    print(f"📅 Check Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 GABRIEL Root: {gabriel_root}")
    print("=" * 80)
    
    total_systems = 0
    found_systems = 0
    missing_systems = []
    
    for category, system_list in systems.items():
        print(f"\n{category}")
        print("-" * 80)
        
        for system_file, description in system_list:
            total_systems += 1
            file_path = gabriel_root / system_file
            
            if file_path.exists():
                found_systems += 1
                size_kb = file_path.stat().st_size / 1024
                
                # Count lines
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = len(f.readlines())
                    
                    status = f"✅ {size_kb:7.1f}KB | {lines:5} lines"
                except:
                    status = f"✅ {size_kb:7.1f}KB"
                
                # Highlight X1000 systems
                if "X1000" in system_file:
                    print(f"   ⚛️  {status} | {system_file:40} | {description}")
                else:
                    print(f"   📦 {status} | {system_file:40} | {description}")
            else:
                missing_systems.append((category, system_file))
                print(f"   ❌ MISSING   | {system_file:40} | {description}")
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print(f"✅ Found: {found_systems}/{total_systems} systems ({found_systems/total_systems*100:.1f}%)")
    
    if missing_systems:
        print(f"\n❌ Missing Systems ({len(missing_systems)}):")
        for category, system in missing_systems:
            print(f"   • {system} ({category})")
    else:
        print("\n🎉 ALL SYSTEMS OPERATIONAL! 🎉")
    
    # X1000 specific stats
    x1000_count = sum(1 for _, systems in systems.items() for file, _ in systems if "X1000" in file and (gabriel_root / file).exists())
    print(f"\n⚛️  X1000 Systems: {x1000_count}")
    print(f"📦 Classic Systems: {found_systems - x1000_count}")
    
    # Quick launch commands
    print("\n" + "=" * 80)
    print("🚀 QUICK LAUNCH COMMANDS")
    print("=" * 80)
    print("# X1000 Supreme Executor (Execute everything)")
    print("python3 X1000_SUPREME_EXECUTOR.py")
    print("\n# X1000 Supreme Integration (Create network)")
    print("python3 X1000_SUPREME_INTEGRATION.py")
    print("\n# X1000 Master Launcher (After integration)")
    print("python3 X1000_MASTER_LAUNCHER.py")
    print("\n# X1000 CODEBEAST Integration")
    print("python3 X1000_CODEBEAST_ULTIMATE.py")
    
    # Check for generated files
    print("\n" + "=" * 80)
    print("📄 GENERATED FILES CHECK")
    print("=" * 80)
    
    generated_files = [
        "X1000_MASTER_LAUNCHER.py",
        "X1000_AGENT_NETWORK.json",
        "X1000_INTEGRATION_REPORT.json",
        "X1000_FIX_SHELL_PERMANENT.sh",
        "X1000_PYTHON_EXEC_SAFE.py",
        "X1000_ACCESS_OUTSIDE_WORKSPACE.py",
        "X1000_CHECK_DOCKER.py",
    ]
    
    for gen_file in generated_files:
        file_path = gabriel_root / gen_file
        if file_path.exists():
            print(f"   ✅ {gen_file}")
        else:
            print(f"   ⏳ {gen_file} (will be created by integration)")
    
    print("\n" + "=" * 80)
    print("✨ STATUS CHECK COMPLETE ✨")
    print("=" * 80)

if __name__ == '__main__':
    check_all_x1000_systems()
