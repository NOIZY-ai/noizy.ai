# GABRIEL File Suite

**Production-Ready File Intelligence System for Network Drives**

A comprehensive Python suite for intelligent file management across GABRIEL and network drives. Features deep scanning, AI-powered classification, smart organization, duplicate detection, and real-time dashboards.

---

## 🌟 Features

### 1. **DeepScan** - Intelligent File Crawler
- ✅ Multi-threaded parallel scanning (8+ workers)
- ✅ SHA256 hashing for deduplication
- ✅ Content signature analysis (first 1KB)
- ✅ Comprehensive metadata extraction
- ✅ SQLite database storage
- ✅ Progress tracking and resumable scans

### 2. **SenseMaker** - AI Classification System
- ✅ Claude AI integration for smart categorization
- ✅ Rule-based fallback classification
- ✅ Dynamic category evolution
- ✅ Confidence scoring
- ✅ Batch processing support
- ✅ Category: Audio, Design, Code, Documents, Video, Archives, Misc

### 3. **HiveSort** - File Organization Engine
- ✅ Multiple organization modes:
  - **Symlink** (recommended - no space used)
  - **Copy** (mirror files)
  - **Move** (relocate files)
  - **Hardlink** (space-efficient copies)
- ✅ Category-based or extension-based organization
- ✅ Preserve directory structure option
- ✅ Automatic conflict resolution
- ✅ Dry-run mode for safety

### 4. **Duplicate Detection**
- ✅ Hash-based duplicate finding
- ✅ Wasted space calculation
- ✅ Multiple handling strategies:
  - List duplicates
  - Keep newest
  - Keep largest
  - Delete all but one
- ✅ Dry-run support

### 5. **Interactive Dashboards**
- ✅ **FastAPI** REST API backend
- ✅ **Streamlit** web interface
- ✅ Real-time statistics
- ✅ Visual analytics (charts, graphs)
- ✅ File search and filtering
- ✅ Category management

### 6. **Automation Ready**
- ✅ Nightly automation scripts
- ✅ Cron job templates
- ✅ Automatic backups
- ✅ Cloud sync preparation
- ✅ Logging and monitoring

---

## 📦 Installation

### Prerequisites
- Python 3.9+
- macOS, Linux, or Windows
- Network drives mounted

### Quick Setup

```bash
# Clone or download the suite
cd gabriel_file_suite

# Run setup script
chmod +x scripts/setup.sh
./scripts/setup.sh

# Activate environment
source venv/bin/activate

# Copy and configure
cp config/config.example.yaml config/config.yaml
# Edit config.yaml with your volume paths

# Optional: Set API key for AI classification
export ANTHROPIC_API_KEY='your-api-key-here'
```

### Manual Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make CLI executable
chmod +x gabriel.py
```

---

## 🚀 Quick Start

### 1. Scan a Volume

```bash
# Scan GABRIEL drive
./gabriel.py scan /Volumes/GABRIEL --database gabriel.db --workers 8

# With duplicate detection
./gabriel.py scan /Volumes/GABRIEL --database gabriel.db --find-duplicates

# Verbose output
./gabriel.py scan /Volumes/GABRIEL --database gabriel.db --verbose
```

### 2. Classify Files

```bash
# Rule-based classification (fast, no API key needed)
./gabriel.py classify gabriel.db --batch 500

# AI-powered classification (requires ANTHROPIC_API_KEY)
./gabriel.py classify gabriel.db --use-ai --batch 100

# Export category mapping
./gabriel.py classify gabriel.db --export categories.json
```

### 3. Organize Files

```bash
# Dry-run (safe - shows what would happen)
./gabriel.py organize gabriel.db /Volumes/GABRIEL/Organized --mode symlink --dry-run

# Create symlink organization (no space used)
./gabriel.py organize gabriel.db /Volumes/GABRIEL/Organized --mode symlink

# Copy files (mirror)
./gabriel.py organize gabriel.db /Volumes/GABRIEL/Organized --mode copy

# Preserve directory structure
./gabriel.py organize gabriel.db /Volumes/GABRIEL/Organized --preserve-structure

# Organize by extension instead of category
./gabriel.py organize gabriel.db /Volumes/GABRIEL/Organized --by-extension
```

### 4. Handle Duplicates

```bash
# List all duplicates
./gabriel.py duplicates gabriel.db --action list

# Keep newest, delete others (dry-run)
./gabriel.py duplicates gabriel.db --action keep_newest --dry-run

# Actually delete (BE CAREFUL!)
./gabriel.py duplicates gabriel.db --action keep_newest
```

### 5. View Statistics

```bash
# Database statistics
./gabriel.py stats gabriel.db
```

---

## 🎨 Dashboard Usage

### Start FastAPI Backend

```bash
# Start API server
python dashboard/api.py

# Or with custom settings
GABRIEL_DB_PATH=/path/to/gabriel.db python dashboard/api.py
```

API will be available at: `http://localhost:8080`

**Endpoints:**
- `GET /` - API info
- `GET /api/stats` - Overall statistics
- `GET /api/categories` - Category breakdown
- `GET /api/duplicates` - Duplicate file groups
- `GET /api/search?query=...` - Search files
- `GET /api/health` - Health check

### Start Streamlit Dashboard

```bash
# Start Streamlit UI
streamlit run dashboard/streamlit_app.py
```

Dashboard will open at: `http://localhost:8501`

**Features:**
- 📊 Overview with charts and metrics
- 🔍 File search with filters
- 📁 Category management
- 🔄 Duplicate viewer
- ⚙️ Action buttons

---

## ⚙️ Configuration

Edit `config/config.yaml` to customize:

```yaml
# Volumes to scan
volumes:
  - name: "GABRIEL"
    path: "/Volumes/GABRIEL"
    scan_enabled: true

# Scanner settings
scanner:
  max_workers: 8
  skip_directories:
    - ".Trash"
    - "node_modules"

# AI Classification
classifier:
  enabled: true
  batch_size: 100
  confidence_threshold: 0.7

# Organization
organizer:
  default_mode: "symlink"
  preserve_structure: false

# Scheduling
schedule:
  scan_interval: "0 2 * * *"  # Daily at 2 AM
```

---

## 🤖 Automation

### Setup Nightly Automation

```bash
# Make script executable
chmod +x scripts/nightly_automation.sh

# Edit script to customize
nano scripts/nightly_automation.sh

# Add to crontab
crontab -e
```

Add this line:
```cron
0 2 * * * /path/to/gabriel_file_suite/scripts/nightly_automation.sh
```

This will run daily at 2 AM and:
1. Scan all configured volumes
2. Classify new files
3. Generate organization plan (dry-run)
4. Find duplicates
5. Create database backup
6. Log everything

### macOS LaunchAgent (Alternative)

Create `~/Library/LaunchAgents/com.gabriel.automation.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.gabriel.automation</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/scripts/nightly_automation.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>2</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.gabriel.automation.plist
```

---

## 📊 Use Cases

### 1. **Creative Studio Organization**
- Scan design assets across multiple drives
- AI-categorize: logos, mockups, photos, videos
- Create symlink structure for fast access
- Find duplicate PSDs eating storage

### 2. **Audio Production Library**
- Index sample libraries on GABRIEL
- Categorize: music, samples, loops, SFX
- Organize by type without moving files
- Identify duplicate audio files

### 3. **Code Project Management**
- Scan development directories
- Categorize by language and project type
- Find duplicate dependencies
- Create organized reference structure

### 4. **Network Drive Cleanup**
- Scan multiple volumes (GABRIEL, OMEN, StudioNet)
- Find duplicates across drives
- Calculate wasted space
- Generate cleanup reports

### 5. **Automated Backup Verification**
- Nightly scans of backup volumes
- Verify file integrity with hashing
- Track changes over time
- Alert on missing files

---

## 🔧 Advanced Features

### Semantic Search (Future)
```python
# Coming soon: Vector similarity search
./gabriel.py search "audio samples jazz" --semantic
```

### Version Control Integration
```python
# Track file versions
./gabriel.py versions --track /path/to/project
```

### Cloud Sync
```yaml
# In config.yaml
cloud_backup:
  enabled: true
  provider: "s3"  # or azure, gcs
  bucket: "gabriel-backup"
```

---

## 🐛 Troubleshooting

### Database locked error
```bash
# Multiple processes accessing database
# Solution: Use different databases or wait for operations to complete
```

### Permission denied
```bash
# Can't read files
# Solution: Run with proper permissions
sudo ./gabriel.py scan /Volumes/GABRIEL --database gabriel.db
```

### API not connecting
```bash
# Check if API is running
curl http://localhost:8080/api/health

# Restart API
killall python
python dashboard/api.py
```

### Out of memory
```bash
# Reduce worker threads
./gabriel.py scan /Volumes/GABRIEL --database gabriel.db --workers 4
```

---

## 📁 Project Structure

```
gabriel_file_suite/
├── gabriel.py              # Main CLI interface
├── src/
│   ├── deepscan.py        # File crawler
│   ├── sensemaker.py      # AI classifier
│   └── hivesort.py        # File organizer
├── dashboard/
│   ├── api.py             # FastAPI backend
│   └── streamlit_app.py   # Streamlit UI
├── config/
│   └── config.example.yaml # Configuration template
├── scripts/
│   ├── setup.sh           # Setup script
│   └── nightly_automation.sh  # Automation script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

---

## 🔐 Security Notes

- **API Keys**: Store `ANTHROPIC_API_KEY` in environment or `.env` file
- **Database**: Contains file paths - keep secure
- **Backups**: Encrypted backups recommended for sensitive data
- **Cloud Sync**: Enable encryption before syncing

---

## 📝 License

This is a custom suite for GABRIEL operations. All rights reserved.

---

## 🤝 Support

For issues or questions:
1. Check `gabriel.py --help` for command help
2. Review configuration in `config.yaml`
3. Check logs in `/Volumes/GABRIEL/gabriel_suite.log`
4. Run with `--verbose` flag for detailed output

---

## 🚀 Roadmap

- [x] Core scanning engine
- [x] AI classification
- [x] Smart organization
- [x] Duplicate detection
- [x] REST API dashboard
- [x] Streamlit UI
- [ ] Semantic vector search
- [ ] Version tracking
- [ ] Cloud backup integration
- [ ] Email notifications
- [ ] Voice control (Lucy integration)
- [ ] React/Next.js dashboard

---

**GABRIEL File Suite** - Intelligent file management for the modern creative workflow.
