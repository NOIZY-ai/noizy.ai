#!/usr/bin/env python3
"""
🚀 QUICK DISTRIBUTE - Execute Master Chain Distribution
"""

import sys
from pathlib import Path

# Add GABRIEL to path
sys.path.insert(0, '/Users/rsp_ms/GABRIEL')

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║  🔗 GABRIEL MASTER CHAIN - QUICK DISTRIBUTION                                 ║
║                                                                                ║
║  This will distribute your Autonomous Learning System across                  ║
║  all connected drives in the master chain for:                                ║
║                                                                                ║
║  ✓ Redundancy    - Multiple backups across drives                            ║
║  ✓ Performance   - High-speed cache on RED DRAGON                            ║
║  ✓ Scalability   - Distributed storage architecture                          ║
║  ✓ Resilience    - Failover between drives                                   ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n📦 DISTRIBUTION PLAN:\n")
print("   12TB 1       → Primary storage (Learning data + Knowledge graph)")
print("   12TB 2       → Backup storage (Full system backup)")
print("   RED DRAGON   → High-speed cache (Active sessions + Analytics)")
print("   GABRIEL_MOUNT → Local mount point (Quick access)")

print("\n📊 CONTENT TO DISTRIBUTE:\n")
print("   ✓ autonomous_learning.py (1,621 lines)")
print("   ✓ RUN_X1000_DEMO.py")
print("   ✓ Learning data directory")
print("   ✓ Knowledge graph (10,000+ concepts)")
print("   ✓ Skill trees (1,000+ skills)")
print("   ✓ AI tutor sessions")
print("   ✓ Achievement system")
print("   ✓ Analytics cache")
print("   ✓ Career optimization data")

print("\n" + "="*80)
choice = input("\nProceed with distribution? (DRY RUN first recommended) [dry/execute/cancel]: ").lower()

if choice == 'cancel':
    print("\n❌ Cancelled")
    sys.exit(0)

dry_run = (choice != 'execute')

if dry_run:
    print("\n⚠️  DRY RUN MODE - No actual changes will be made")
else:
    confirm = input("\n⚠️  EXECUTE MODE - Files will be copied. Continue? (yes/no): ")
    if confirm.lower() != 'yes':
        print("\n❌ Cancelled")
        sys.exit(0)

# Import and run
from distribute_to_drives import DriveDistributor

distributor = DriveDistributor()

print("\n" + "="*80)
print("🚀 STARTING DISTRIBUTION...")
print("="*80)

# Step 1: Create structure
print("\n1️⃣  Creating directory structure...")
result1 = distributor.create_structure(dry_run=dry_run)

# Step 2: Distribute files
print("\n2️⃣  Distributing autonomous learning system...")
source = Path('/Users/rsp_ms/GABRIEL')
result2 = distributor.distribute_autonomous_learning(source, dry_run=dry_run)

# Step 3: Create symlinks
print("\n3️⃣  Creating symlink network...")
result3 = distributor.create_symlinks(dry_run=dry_run)

# Report
print("\n" + "="*80)
print("📊 DISTRIBUTION COMPLETE!")
print("="*80)
print(distributor.generate_report())

if not dry_run:
    # Save report
    report_path = Path('/Users/rsp_ms/GABRIEL/DISTRIBUTION_REPORT.txt')
    report_path.write_text(distributor.generate_report())
    print(f"\n📄 Full report saved: {report_path}")

print("\n✅ MASTER CHAIN DISTRIBUTION FINISHED!")
print("\nYour Autonomous Learning System is now distributed across:")
for drive_id in distributor.stats['drives_used']:
    print(f"   ✓ {drive_id}")
