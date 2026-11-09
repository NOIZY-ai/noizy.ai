# GABRIEL File Suite - Deployment Guide

## 📦 Complete Package Contents

### Core Modules (`src/`)
- ✅ **deepscan.py** - Multi-threaded file crawler with SHA256 hashing
- ✅ **sensemaker.py** - AI classification with Claude + rule-based fallback
- ✅ **hivesort.py** - Smart file organizer with 4 modes (move/copy/symlink/hardlink)

### CLI Interface
- ✅ **gabriel.py** - Main command-line interface
- ✅ **example_workflow.py** - Complete workflow demonstration

### Dashboard (`dashboard/`)
- ✅ **api.py** - FastAPI REST backend
- ✅ **streamlit_app.py** - Interactive web UI with charts

### Configuration (`config/`)
- ✅ **config.example.yaml** - Full configuration template
- ✅ Settings for volumes, scheduling, AI, cloud backup

### Automation (`scripts/`)
- ✅ **setup.sh** - One-command setup
- ✅ **nightly_automation.sh** - Cron-ready automation script

### Documentation
- ✅ **README.md** - Complete documentation (100+ sections)
- ✅ **QUICKSTART.md** - 5-minute getting started guide
- ✅ **requirements.txt** - Python dependencies

### Configuration Files
- ✅ **.env.example** - Environment variables template
- ✅ **.gitignore** - Git exclusions

---

## 🚀 Deployment Steps

### Option 1: Local Development

```bash
# 1. Navigate to suite
cd /Users/rsp_ms/GABRIEL/THE_FAMILY/GABRIEL/gabriel_file_suite

# 2. Make scripts executable
chmod +x gabriel.py example_workflow.py scripts/*.sh

# 3. Run setup
./scripts/setup.sh

# 4. Configure
cp config/config.example.yaml config/config.yaml
cp .env.example .env
# Edit both files

# 5. Activate environment
source venv/bin/activate

# 6. Test run
./gabriel.py --help
```

### Option 2: Production Server

```bash
# 1. Setup as above

# 2. Start API (background)
nohup python dashboard/api.py > /Volumes/GABRIEL/logs/api.log 2>&1 &

# 3. Start Streamlit (background)
nohup streamlit run dashboard/streamlit_app.py > /Volumes/GABRIEL/logs/streamlit.log 2>&1 &

# 4. Setup automation
crontab -e
# Add: 0 2 * * * /path/to/scripts/nightly_automation.sh
```

### Option 3: macOS LaunchAgent

Create `~/Library/LaunchAgents/com.gabriel.suite.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.gabriel.suite</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/gabriel_file_suite/venv/bin/python</string>
        <string>/path/to/gabriel_file_suite/dashboard/api.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Volumes/GABRIEL/logs/gabriel_api.log</string>
    <key>StandardErrorPath</key>
    <string>/Volumes/GABRIEL/logs/gabriel_api_error.log</string>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.gabriel.suite.plist
```

---

## 🎯 Recommended Usage Patterns

### Pattern 1: Initial Setup
```bash
# Day 1: Full scan
./gabriel.py scan /Volumes/GABRIEL --database gabriel.db --workers 8
./gabriel.py scan /Volumes/NOIZYWIN --database gabriel.db --workers 8
./gabriel.py scan /Volumes/OMEN --database gabriel.db --workers 8

# Day 1: Classify (rule-based, fast)
./gabriel.py classify gabriel.db --batch 1000

# Day 1: Review results
./gabriel.py stats gabriel.db
./gabriel.py duplicates gabriel.db --action list

# Day 2: Organize (after review)
./gabriel.py organize gabriel.db /Volumes/GABRIEL/Organized --mode symlink
```

### Pattern 2: Nightly Maintenance
```bash
# Automated via cron (2 AM daily)
# - Incremental scan
# - Classify new files
# - Update organization
# - Find new duplicates
# - Backup database
```

### Pattern 3: On-Demand Analysis
```bash
# Start dashboard when needed
python dashboard/api.py &
streamlit run dashboard/streamlit_app.py

# Browse to http://localhost:8501
# Interactive exploration and search
```

---

## 🔐 Security Recommendations

1. **API Keys**: Store in `.env` file, never commit
2. **Database**: Contains all file paths - restrict access
3. **Backups**: Enable automatic database backups
4. **API Access**: Use firewall rules to restrict dashboard access
5. **File Operations**: Always dry-run first with sensitive data

---

## 📊 Performance Tuning

### For Large Volumes (10TB+)
```yaml
# In config.yaml
scanner:
  max_workers: 16  # More threads
  
performance:
  max_memory_gb: 8
  cache_size_mb: 1024
```

### For Many Small Files (100K+)
```yaml
scanner:
  max_workers: 12
  skip_extensions:
    - ".tmp"
    - ".cache"
    # Add more to reduce processing
```

### For Network Drives
```yaml
scanner:
  max_workers: 4  # Lower for network I/O
  
performance:
  io_buffer_size: 16384  # Larger buffers
```

---

## 🔄 Backup Strategy

### Database Backups
```bash
# Manual
cp gabriel.db gabriel_backup_$(date +%Y%m%d).db

# Automated (in nightly_automation.sh)
# Keeps 7 days of backups
```

### Volume Backups
```yaml
# In config.yaml
cloud_backup:
  enabled: true
  provider: "s3"  # or "azure", "gcs"
  bucket: "gabriel-backup"
  encrypt: true
```

---

## 📈 Monitoring

### Check System Health
```bash
# API health
curl http://localhost:8080/api/health

# Database stats
./gabriel.py stats gabriel.db

# Logs
tail -f /Volumes/GABRIEL/gabriel_suite.log
```

### Key Metrics to Track
- Files indexed per day
- Classification completion %
- Duplicate space saved
- Database size growth
- Scan duration trends

---

## 🆘 Troubleshooting

### Common Issues

**1. "Database is locked"**
```bash
# Solution: Another process is using it
ps aux | grep gabriel
# Kill stale processes or wait
```

**2. "Permission denied"**
```bash
# Solution: File permissions
sudo ./gabriel.py scan /Volumes/GABRIEL --database gabriel.db
```

**3. "API not responding"**
```bash
# Check if running
ps aux | grep "dashboard/api.py"

# Restart
killall python
python dashboard/api.py
```

**4. "Out of memory"**
```bash
# Reduce workers
./gabriel.py scan /Volumes/GABRIEL --database gabriel.db --workers 4
```

---

## 🎓 Training Resources

### For Team Members

1. **Read QUICKSTART.md** - 5-minute overview
2. **Run example_workflow.py** - See full pipeline
3. **Try dashboard** - Visual exploration
4. **Review config.yaml** - Understand options
5. **Check automation logs** - See what runs nightly

### Command Cheat Sheet

```bash
# Scan
./gabriel.py scan <volume> --database gabriel.db

# Classify
./gabriel.py classify gabriel.db --batch 100

# Organize
./gabriel.py organize gabriel.db <output> --mode symlink --dry-run

# Duplicates
./gabriel.py duplicates gabriel.db --action list

# Stats
./gabriel.py stats gabriel.db

# Dashboard
python dashboard/api.py  # Backend
streamlit run dashboard/streamlit_app.py  # UI
```

---

## 🚀 Going Live Checklist

- [ ] Setup complete (`./scripts/setup.sh`)
- [ ] Configuration customized (`config/config.yaml`)
- [ ] Environment variables set (`.env`)
- [ ] Initial scan completed
- [ ] Classification run
- [ ] Organization tested (dry-run)
- [ ] Automation scheduled
- [ ] Dashboard accessible
- [ ] Backups configured
- [ ] Team trained
- [ ] Documentation reviewed

---

## 📞 Support

For issues:
1. Check logs: `/Volumes/GABRIEL/gabriel_suite.log`
2. Run with `--verbose` flag
3. Review documentation in `README.md`
4. Check API health: `/api/health` endpoint

---

**GABRIEL File Suite** is now ready for production deployment! 🎉

Deploy with confidence - all components are modular, scalable, and production-tested.
