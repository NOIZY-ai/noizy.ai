# GABRIEL File Suite - Quick Start Guide

## 🚀 5-Minute Setup

### 1. Install

```bash
cd gabriel_file_suite
chmod +x scripts/setup.sh
./scripts/setup.sh
source venv/bin/activate
```

### 2. Configure

```bash
cp config/config.example.yaml config/config.yaml
cp .env.example .env
# Edit config.yaml and .env with your settings
```

### 3. First Scan

```bash
# Scan your GABRIEL drive
./gabriel.py scan /Volumes/GABRIEL --database gabriel.db --workers 8
```

### 4. Classify Files

```bash
# Fast rule-based classification
./gabriel.py classify gabriel.db --batch 500

# Or with AI (set ANTHROPIC_API_KEY first)
export ANTHROPIC_API_KEY='sk-...'
./gabriel.py classify gabriel.db --use-ai --batch 100
```

### 5. View Results

```bash
# Statistics
./gabriel.py stats gabriel.db

# Find duplicates
./gabriel.py duplicates gabriel.db --action list
```

### 6. Start Dashboard

```bash
# Terminal 1: API
python dashboard/api.py

# Terminal 2: UI
streamlit run dashboard/streamlit_app.py
```

Open browser: `http://localhost:8501`

---

## 📋 Common Commands

### Scan Multiple Volumes
```bash
./gabriel.py scan /Volumes/GABRIEL --database gabriel.db
./gabriel.py scan /Volumes/NOIZYWIN --database gabriel.db
./gabriel.py scan /Volumes/OMEN --database gabriel.db
```

### Organize Files (Safe Symlink Mode)
```bash
# Dry-run first
./gabriel.py organize gabriel.db /Volumes/GABRIEL/Organized --mode symlink --dry-run

# Then do it
./gabriel.py organize gabriel.db /Volumes/GABRIEL/Organized --mode symlink
```

### Search Files
```bash
# Via API
curl "http://localhost:8080/api/search?query=logo&category=Design"
```

### Automation Setup
```bash
# Edit automation script
nano scripts/nightly_automation.sh

# Add to crontab
crontab -e
# Add: 0 2 * * * /path/to/scripts/nightly_automation.sh
```

---

## ⚡ Pro Tips

1. **Use Symlinks** - Organize without using extra space
2. **Dry-Run First** - Always test with `--dry-run`
3. **Batch Processing** - Classify in batches for AI quota management
4. **Regular Scans** - Set up nightly automation
5. **Backup Database** - Your metadata is valuable!

---

## 🆘 Need Help?

- CLI help: `./gabriel.py --help`
- Command help: `./gabriel.py scan --help`
- Check logs: `tail -f /Volumes/GABRIEL/gabriel_suite.log`
- API health: `curl http://localhost:8080/api/health`

---

**You're ready to go! 🎉**
