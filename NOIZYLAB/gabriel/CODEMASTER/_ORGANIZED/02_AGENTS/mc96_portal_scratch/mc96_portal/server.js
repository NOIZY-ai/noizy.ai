const express = require('express');
const cors = require('cors');
const { spawn, exec } = require('child_process');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3001;

// Paths to MEMCELL resources
// Mapped to the NOIZYLAB location
const NOIZYLAB_PATH = '/Users/m2ultra/.gemini/antigravity/scratch/NOIZYLAB';
const MEMCELL_DB_PATH = path.join(NOIZYLAB_PATH, 'memcell_db.json');
const MEMCELL_SCRIPT_PATH = path.join(NOIZYLAB_PATH, 'AI_INTEGRATION_SUITE/MEMCELL_CORE.py');

app.use(cors());
app.use(express.json());

// API: Get Memory DB
app.get('/api/memory', (req, res) => {
    fs.readFile(MEMCELL_DB_PATH, 'utf8', (err, data) => {
        if (err) {
            console.error('Error reading DB:', err);
            return res.status(500).json({ error: 'Failed to read memory database' });
        }
        try {
            const json = JSON.parse(data);
            res.json(json);
        } catch (e) {
            res.status(500).json({ error: 'Invalid JSON in database' });
        }
    });
});

// API: Add Thought/Memory via Python Script
app.post('/api/memory', (req, res) => {
    const { content, topic, author, subject } = req.body;
    
    if (!content) return res.status(400).json({ error: 'Content required' });

    // Usage: python3 MEMCELL_CORE.py add "Content" "Topic" "Author" "Subject"
    const args = ['add', content, topic || 'General', author || 'MC96_PORTAL', subject || 'System'];
    
    // Run the python script
    const py = spawn('python3', [MEMCELL_SCRIPT_PATH, ...args], {
        cwd: path.dirname(MEMCELL_SCRIPT_PATH) // Run from the script's dir for relative paths (if any)
    });

    let output = '';
    py.stdout.on('data', (data) => output += data.toString());
    py.stderr.on('data', (data) => console.error(`Py Error: ${data}`));

    py.on('close', (code) => {
        if (code === 0) {
            res.json({ success: true, output: output.trim() });
        } else {
            res.status(500).json({ error: 'Python script failed', details: output });
        }
    });
});

// API: System Status
app.get('/api/status', (req, res) => {
    res.json({
        status: 'GOD_MODE',
        latency: 'ZERO', // Hardcoded perfection per user request
        agents: {
            GABRIEL: 'Active',
            SHIRL: 'Active',
            ENGR: 'Active'
        },
        timestamp: new Date().toISOString()
    });
});

app.listen(PORT, () => {
    console.log(`🚀 MC96 Mission Control Backend running on port ${PORT}`);
    console.log(`🔗 Connected to MEMCELL at: ${MEMCELL_DB_PATH}`);
});
