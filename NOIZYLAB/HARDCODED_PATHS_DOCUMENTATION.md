# Hardcoded Paths Documentation

## Overview
This document tracks hardcoded paths found in the NOIZYLAB repository that may need to be updated for portability across different machines and environments.

## Critical Hardcoded Paths

### 1. User-Specific macOS Paths
**Pattern**: `/Users/m2ultra/*`
**Found in**: 798+ files across the repository
**Impact**: Code won't run on other machines/environments

**Example locations**:
- Python scripts in `gabriel/` directory
- Shell scripts throughout the repository
- Configuration files
- Documentation files

**Recommended fix**:
- Replace with environment variables (e.g., `$HOME`, `$USER`)
- Use relative paths where possible
- Create a configuration file with path mappings

### 2. Broken Symlinks (FIXED)
**Status**: ✅ **RESOLVED**
- `OneDrive` → `/Users/m2ultra/Library/CloudStorage/OneDrive-Personal(2)` - **REMOVED**
- `gabriel/CODEMASTER/_ORGANIZED/05_TOOLS/bin_tools/gorunfree` - **REMOVED**

### 3. Large Binary Files
**Pattern**: `gabriel/golang/*.json`
**Impact**: Slow Git operations, repository bloat

**Files identified**:
- `gabriel/golang/brain.json` (42MB)
- `gabriel/golang/memcell_db_*.json` (13-16MB each)

**Status**: ✅ Added to `.gitignore`

## Recommendations for Future Development

### Use Environment Variables
```bash
# Instead of:
/Users/m2ultra/NOIZYLAB/scripts/setup.sh

# Use:
${NOIZYLAB_HOME}/scripts/setup.sh
# or
${HOME}/NOIZYLAB/scripts/setup.sh
```

### Configuration File Pattern
Create a `config/paths.yaml` or `.env` file:
```yaml
project_root: ${HOME}/NOIZYLAB
data_dir: ${HOME}/NOIZYLAB/data
scripts_dir: ${HOME}/NOIZYLAB/scripts
```

### Use Relative Paths
When working within the repository, prefer relative paths:
```python
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
```

## Files Requiring Manual Review

The following file types contain hardcoded paths that should be reviewed:
1. Python scripts (`.py`)
2. Shell scripts (`.sh`)
3. Configuration files (`.json`, `.yaml`, `.toml`)
4. Documentation (`.md`)

## Migration Strategy

### Phase 1: Critical Scripts ⏳ PENDING
- Identify top 10 most-used scripts with hardcoded paths
- Update them to use environment variables
- Test on different machines

### Phase 2: Configuration Files ⏳ PENDING
- Centralize path configuration
- Create `.env.template` files
- Document required environment variables

### Phase 3: Bulk Update ⏳ PENDING
- Use automated tools to replace remaining hardcoded paths
- Review and test changes
- Update documentation

## Completed Cleanup Actions

✅ **Removed broken symlinks** (2 files)
✅ **Removed empty placeholder files** (10 files)
✅ **Quarantined files with syntax errors** (2 files)
✅ **Fixed shell script permissions** (168 files)
✅ **Removed duplicate directories** (gabriel/mc96_projects/GABRIEL - 252 files, 1.8MB)
✅ **Updated .gitignore** for large JSON files

## Next Steps

1. **Immediate**: Review scripts in `gabriel/bin/` for hardcoded paths
2. **Short-term**: Create environment variable configuration
3. **Long-term**: Implement automated path checking in CI/CD

---

**Last Updated**: 2026-02-10
**Maintained by**: CODECLEANER Agent
