#!/usr/bin/env python3
"""
Local GABRIEL deployment (no network mounting required)
Creates organized structure in current directory
"""

import shutil
from pathlib import Path
from datetime import datetime

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║  🚀 GABRIEL LOCAL DEPLOYMENT                                                   ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

# Create local deployment
deploy_dir = Path('/Users/rsp_ms/GABRIEL/GABRIEL_DEPLOY')
deploy_dir.mkdir(exist_ok=True)

print(f"\n📁 Creating deployment at: {deploy_dir}\n")

# Structure
dirs = ['core', 'agents', 'docs', 'logs', 'config']
for d in dirs:
    (deploy_dir / d).mkdir(exist_ok=True)
    print(f"✓ Created: {d}/")

print("\n📦 Copying files...\n")

# Files to deploy
gabriel_root = Path('/Users/rsp_ms/GABRIEL')
files = {
    'core': [
        'gabriel_ultimate.py',
        'file_organizer.py',
        'migration_orchestrator.py',
        'diagnostic_fix.py',
        'organize_12tb.py',
        'gabriel_deployer.py'
    ],
    'docs': [
        '12TB_ORGANIZATION_PLAN.md',
        'EXECUTION_READY.md',
        'QUICKSTART.md'
    ]
}

deployed = 0
for dest_dir, file_list in files.items():
    for filename in file_list:
        src = gabriel_root / filename
        if src.exists():
            dst = deploy_dir / dest_dir / filename
            shutil.copy2(src, dst)
            print(f"✓ {filename} → {dest_dir}/")
            deployed += 1

# Create requirements
req_file = deploy_dir / 'requirements.txt'
req_file.write_text("""# GABRIEL Requirements
psutil>=5.9.0
aiohttp>=3.8.0
websockets>=10.0
Pillow>=9.0.0
mutagen>=1.45.0
black>=22.0.0
python-dotenv>=0.20.0
pyyaml>=6.0
rich>=12.0.0
""")
print("\n✓ Created: requirements.txt")

# Create README
readme = deploy_dir / 'README.md'
readme.write_text(f"""# GABRIEL Deployment

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Location:** `{deploy_dir}`

## Quick Start

```bash
cd {deploy_dir}

# Install dependencies
pip3 install -r requirements.txt

# Run GABRIEL
python3 core/gabriel_ultimate.py

# Organize music
python3 core/organize_12tb.py

# Run diagnostics
python3 core/diagnostic_fix.py
```

## Structure

- `core/` - Main systems
- `docs/` - Documentation
- `logs/` - System logs
- `config/` - Configuration files

## Files Deployed

{deployed} files deployed successfully ✅
""")
print("✓ Created: README.md")

print("\n" + "=" * 80)
print("✅ DEPLOYMENT COMPLETE!")
print("=" * 80)
print(f"\n📍 Location: {deploy_dir}")
print(f"📦 Files deployed: {deployed}")
print(f"\n🚀 To run:")
print(f"   cd {deploy_dir}")
print(f"   python3 core/gabriel_ultimate.py")
print("\n✨ Done!")
