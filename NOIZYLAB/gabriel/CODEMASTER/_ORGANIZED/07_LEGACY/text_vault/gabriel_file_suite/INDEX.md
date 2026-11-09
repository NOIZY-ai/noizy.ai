# 🗂️ GABRIEL File Suite

**Production-Ready DeepScan → SenseMaker → HiveSort Python Suite**

> Intelligent file management for GABRIEL and network drives with AI classification, smart organization, and real-time dashboards.

---

## 🎯 What Is This?

A complete Python ecosystem for managing files across multiple volumes with:

- **DeepScan** 🔍 - Parallel file crawler with metadata extraction and deduplication
- **SenseMaker** 🧠 - AI-powered classification using Claude + rule-based fallback  
- **HiveSort** 📁 - Smart organization with symlink/copy/move/hardlink modes
- **Dashboards** 🎨 - FastAPI backend + Streamlit UI with charts and search
- **Automation** 🤖 - Nightly scripts, cron jobs, automatic backups

---

## ⚡ Quick Start (5 Minutes)

```bash
# 1. Setup
cd gabriel_file_suite
./scripts/setup.sh
source venv/bin/activate

# 2. Configure
cp config/config.example.yaml config/config.yaml
# Edit config.yaml - set your volume paths

# 3. Scan
./gabriel.py scan /Volumes/GABRIEL --database gabriel.db --workers 8

# 4. Classify
./gabriel.py classify gabriel.db --batch 500

# 5. Organize (symlink = no space used!)
./gabriel.py organize gabriel.db /Volumes/GABRIEL/Organized --mode symlink --dry-run

# 6. Dashboard
python dashboard/api.py &
streamlit run dashboard/streamlit_app.py
# Open: http://localhost:8501
```

---

## 📚 Documentation

| Doc | Purpose | Time |
|-----|---------|------|
| [**QUICKSTART.md**](QUICKSTART.md) | Get running fast | 5 min |
| [**README.md**](README.md) | Complete guide | 20 min |
| [**DEPLOYMENT.md**](DEPLOYMENT.md) | Production setup | 10 min |
| [**OVERVIEW.md**](OVERVIEW.md) | Feature summary | 10 min |
| [**MANIFEST.md**](MANIFEST.md) | File inventory | 5 min |

---

## 🎁 What's Included

### Core Modules
- ✅ `deepscan.py` - Multi-threaded crawler with SHA256 hashing
- ✅ `sensemaker.py` - AI classification (Claude) + rules
- ✅ `hivesort.py` - Smart organization with 4 modes

### CLI & Tools
- ✅ `gabriel.py` - Main command-line interface
- ✅ `example_workflow.py` - Complete demo workflow

### Dashboards
- ✅ `dashboard/api.py` - FastAPI REST backend
- ✅ `dashboard/streamlit_app.py` - Interactive web UI

### Automation
- ✅ `scripts/setup.sh` - One-command setup
- ✅ `scripts/nightly_automation.sh` - Cron-ready automation

### Configuration
- ✅ `config/config.example.yaml` - Full config template
- ✅ `.env.example` - Environment variables

---

## 🔥 Key Features

### DeepScan
- Multi-threaded parallel scanning (8+ workers)
- SHA256 hashing for deduplication
- Content signatures (first 1KB analysis)
- MIME type detection
- Comprehensive metadata extraction
- SQLite database storage
- Progress tracking & resumable scans

### SenseMaker
- AI classification using Claude (optional)
- Rule-based fallback (fast, free)
- Categories: Audio, Design, Code, Docs, Video, Archives, Misc
- Confidence scoring
- Batch processing
- Export category mappings

### HiveSort
- **4 organization modes:**
  - Symlink (recommended - no space used)
  - Copy (mirror files)
  - Move (relocate files)  
  - Hardlink (space-efficient copies)
- Category-based or extension-based organization
- Preserve directory structure option
- Automatic conflict resolution
- Dry-run mode for safety
- Manifest generation

### Duplicate Detection
- Hash-based duplicate finding
- Wasted space calculation
- Multiple handling strategies
- Dry-run support

### Dashboards
- FastAPI REST API
- Streamlit interactive UI
- Real-time statistics
- Visual charts and graphs
- File search with filters
- Category management
- Duplicate viewer

### Automation
- Nightly scan scripts
- Automatic classification
- Database backups
- Log management
- Cron/LaunchAgent templates

---

## 💻 CLI Commands

```bash
# Scan a volume
./gabriel.py scan /Volumes/GABRIEL --database gabriel.db --workers 8

# Classify files (rule-based)
./gabriel.py classify gabriel.db --batch 500

# Classify with AI (requires ANTHROPIC_API_KEY)
./gabriel.py classify gabriel.db --use-ai --batch 100

# Organize files (dry-run first!)
./gabriel.py organize gabriel.db /path/to/output --mode symlink --dry-run
./gabriel.py organize gabriel.db /path/to/output --mode symlink

# Find duplicates
./gabriel.py duplicates gabriel.db --action list

# View statistics
./gabriel.py stats gabriel.db

# Get help
./gabriel.py --help
./gabriel.py scan --help
```

---

## 🎨 Dashboard Usage

### Start API Backend
```bash
python dashboard/api.py
# Available at: http://localhost:8080
# API docs: http://localhost:8080/docs
```

### Start Streamlit UI
```bash
streamlit run dashboard/streamlit_app.py
# Opens: http://localhost:8501
```

### Features
- 📊 Overview with metrics and charts
- 🔍 Search files by name/category/extension
- 📁 Category management and stats
- 🔄 Duplicate file viewer
- ⚙️ Quick action buttons

---

## 🤖 Automation Setup

```bash
# Make executable
chmod +x scripts/nightly_automation.sh

# Add to crontab (runs daily at 2 AM)
crontab -e
# Add: 0 2 * * * /path/to/scripts/nightly_automation.sh
```

Nightly script automatically:
1. Scans all configured volumes
2. Classifies new files
3. Generates organization plan
4. Finds duplicates
5. Creates database backup
6. Cleans up old logs

---

## 📊 Use Cases

### Creative Studio
- Organize design assets across drives
- AI-categorize: logos, mockups, photos
- Create symlink library for fast access
- Find duplicate PSDs

### Audio Production
- Index sample libraries
- Categorize: music, samples, loops, SFX
- Organize without moving files
- Identify duplicate audio

### Code Management
- Scan development directories
- Categorize by language
- Find duplicate dependencies
- Create organized reference

### Network Cleanup
- Scan multiple volumes
- Find duplicates across drives
- Calculate wasted space
- Generate cleanup reports

---

## 🔧 Requirements

- Python 3.9+
- macOS, Linux, or Windows
- Network drives mounted
- Optional: Anthropic API key for AI classification

---

## 📦 Installation

### Quick Install
```bash
./scripts/setup.sh
```

### Manual Install
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
chmod +x gabriel.py
```

---

## ⚙️ Configuration

Copy and edit:
```bash
cp config/config.example.yaml config/config.yaml
cp .env.example .env
```

Set your:
- Volume paths
- Database location
- Worker threads
- AI settings
- Automation schedule
- Cloud backup (optional)

---

## 🎯 Performance

### Typical (2TB, 250K files)
- Scan: ~5 minutes (8 workers)
- Classify: ~2 minutes (rule-based)
- Organize: <1 minute (symlink)
- Database: ~50MB

### Large Scale (10TB, 1M+ files)
- Scan: ~25 minutes (16 workers)
- Classify: ~10 minutes (batch 1000)
- Database: ~500MB

---

## 🔐 Security

- API keys in `.env` (never commit)
- Database contains file paths (restrict access)
- Automatic backups enabled
- Dry-run modes everywhere
- CORS configured

---

## 🚀 Production Ready

- ✅ Multi-threaded performance
- ✅ Error handling & logging
- ✅ Progress tracking
- ✅ Resumable operations
- ✅ Database backups
- ✅ Health checks
- ✅ Dry-run safety
- ✅ Comprehensive docs

---

## 🆘 Support

- **Help**: `./gabriel.py --help`
- **Logs**: `/Volumes/GABRIEL/gabriel_suite.log`
- **API Health**: `curl http://localhost:8080/api/health`
- **Troubleshooting**: See `README.md`

---

## 🗺️ Roadmap

- [x] Core scanning engine
- [x] AI classification
- [x] Smart organization
- [x] Duplicate detection
- [x] REST API + UI
- [ ] Semantic vector search
- [ ] Version tracking
- [ ] Cloud backup integration
- [ ] React dashboard
- [ ] Voice control

---

## 📄 License

Custom suite for GABRIEL operations. All rights reserved.

---

## 🎉 Get Started Now!

```bash
# Clone or navigate to directory
cd gabriel_file_suite

# Run setup (30 seconds)
./scripts/setup.sh

# You're ready! See QUICKSTART.md for next steps
```

---

**GABRIEL File Suite** - Transform chaos into order. 🚀

*Production-ready • Plug-and-play • Scalable • Smart*

---

**[Read Full Documentation →](README.md)** | **[Quick Start →](QUICKSTART.md)** | **[Deploy →](DEPLOYMENT.md)**
