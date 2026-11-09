/**
 * MC96 Mission Control - Application Logic
 * ===========================================
 * GORUNFREE!!! 🚀
 */

// ========================
// Data Configuration
// ========================

const volumeData = [
    { name: '12TB', size: '11 TB', used: '8.3 TB', free: '2.6 TB', percent: 77, status: 'watch' },
    { name: '6TB', size: '5.5 TB', used: '4.7 TB', free: '817 GB', percent: 86, status: 'watch' },
    { name: '4TB Big Fish', size: '3.6 TB', used: '1.7 TB', free: '1.9 TB', percent: 48, status: 'healthy' },
    { name: '4TB Blue Fish', size: '3.6 TB', used: '3.6 TB', free: '64 GB', percent: 99, status: 'critical' },
    { name: '4TB FISH SG', size: '3.6 TB', used: '2.9 TB', free: '710 GB', percent: 81, status: 'watch' },
    { name: '4TB Lacie', size: '3.6 TB', used: '488 GB', free: '3.2 TB', percent: 14, status: 'healthy' },
    { name: '4TBSG', size: '3.6 TB', used: '923 GB', free: '2.7 TB', percent: 25, status: 'healthy' },
    { name: '4TB_02', size: '3.6 TB', used: '167 GB', free: '3.5 TB', percent: 5, status: 'healthy' },
    { name: '4TB_Utility', size: '3.6 TB', used: '1.3 TB', free: '2.3 TB', percent: 36, status: 'healthy' },
    { name: 'EW', size: '931 GB', used: '865 GB', free: '66 GB', percent: 93, status: 'critical' },
    { name: 'FISH', size: '1.8 TB', used: '1.6 TB', free: '225 GB', percent: 88, status: 'watch' },
    { name: 'MAG 4TB', size: '3.6 TB', used: '3.4 TB', free: '265 GB', percent: 93, status: 'critical' },
    { name: 'RED DRAGON', size: '3.6 TB', used: '356 GB', free: '3.3 TB', percent: 10, status: 'healthy' },
    { name: 'RSP', size: '1.8 TB', used: '1.6 TB', free: '225 GB', percent: 88, status: 'watch' },
    { name: 'SAMPLE_MASTER', size: '1.8 TB', used: '62 GB', free: '1.8 TB', percent: 4, status: 'healthy' },
    { name: 'SIDNEY', size: '2.7 TB', used: '2.4 TB', free: '315 GB', percent: 89, status: 'watch' },
    { name: 'SOUND_DESIGN', size: '1.8 TB', used: '14 GB', free: '1.8 TB', percent: 1, status: 'healthy' }
];

const alertsData = [
    { type: 'critical', title: '4TB Blue Fish (99% FULL)', message: 'ACTION: Move content to 4TB_02 or 4TB Lacie' },
    { type: 'critical', title: 'EW (93% FULL)', message: 'EastWest dedicated - OK but watch closely' },
    { type: 'critical', title: 'MAG 4TB (93% FULL)', message: 'Consider moving EZDrummer to consolidate' }
];

const originalsData = [
    'Deep_Transportation_Tone.aif',
    'Tones_from_Es_Vedra_1.aif',
    'hungernorm.aif',
    'detroit.aif',
    'i_just_wanna_dance.aif',
    'INHARMX_3.aif',
    'dieter_sample.aif',
    'whoknowas.aif',
    'XF_SLICE_1.aif',
    'XF_SLICE_2.aif',
    'XF_SLICE_3.aif',
    'STRUM3.aif'
];

// ========================
// DOM Elements
// ========================

const clockEl = document.getElementById('clock');
const volumeGridEl = document.getElementById('volume-grid');
const alertListEl = document.getElementById('alert-list');
const originalsListEl = document.getElementById('originals-list');
const consoleOutputEl = document.getElementById('console-output');

// ========================
// Initialization
// ========================

document.addEventListener('DOMContentLoaded', () => {
    initClock();
    renderVolumes();
    renderAlerts();
    renderOriginals();
    log('[READY] All systems operational', 'success');
});

// ========================
// Clock
// ========================

function initClock() {
    updateClock();
    setInterval(updateClock, 1000);
}

function updateClock() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const mins = String(now.getMinutes()).padStart(2, '0');
    const secs = String(now.getSeconds()).padStart(2, '0');
    clockEl.textContent = `${hours}:${mins}:${secs}`;
}

// ========================
// Volume Rendering
// ========================

function renderVolumes() {
    volumeGridEl.innerHTML = volumeData.map(vol => `
        <div class="volume-card ${vol.status}">
            <div class="volume-name">${vol.name}</div>
            <div class="volume-bar">
                <div class="volume-fill" style="width: ${vol.percent}%"></div>
            </div>
            <div class="volume-info">
                <span>${vol.percent}%</span>
                <span>${vol.free} free</span>
            </div>
        </div>
    `).join('');
}

// ========================
// Alerts Rendering
// ========================

function renderAlerts() {
    alertListEl.innerHTML = alertsData.map(alert => `
        <div class="alert-item ${alert.type}">
            <div class="alert-title">🔴 ${alert.title}</div>
            <div class="alert-message">${alert.message}</div>
        </div>
    `).join('');
}

// ========================
// Originals Rendering
// ========================

function renderOriginals() {
    originalsListEl.innerHTML = originalsData.map(file => `
        <div class="original-item">🎵 ${file}</div>
    `).join('');
}

// ========================
// Console Logging
// ========================

function log(message, type = '') {
    const entry = document.createElement('div');
    entry.className = `log-entry ${type}`;
    entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
    consoleOutputEl.appendChild(entry);
    consoleOutputEl.scrollTop = consoleOutputEl.scrollHeight;
}

function clearConsole() {
    consoleOutputEl.innerHTML = '';
    log('[CLEAR] Console cleared', 'info');
}

// ========================
// Action Handlers
// ========================

function runUpgrade() {
    log('[ACTION] Starting Quality Upgrade & Consolidation...', 'info');
    
    // Simulate progress
    setTimeout(() => log('[SCAN] Loading registry data...', 'info'), 500);
    setTimeout(() => log('[PROCESS] Analyzing 21.9M+ files...', 'info'), 1500);
    setTimeout(() => log('[UPGRADE] Replacing lower quality duplicates...', 'warning'), 3000);
    setTimeout(() => log('[SUCCESS] ✅ Quality upgrade complete!', 'success'), 5000);
    
    showNotification('Quality Upgrade Started', 'Analyzing files for quality consolidation...');
}

function runScan() {
    log('[ACTION] Initiating Deep Scan...', 'info');
    
    setTimeout(() => log('[SCAN] Scanning all 20 volumes...', 'info'), 500);
    setTimeout(() => log('[SCAN] Checking file integrity...', 'info'), 2000);
    setTimeout(() => log('[SCAN] Building file index...', 'info'), 4000);
    setTimeout(() => log('[SUCCESS] ✅ Deep scan complete!', 'success'), 6000);
    
    showNotification('Deep Scan Started', 'Scanning all volumes for analysis...');
}

function findOriginals() {
    log('[ACTION] Searching for ROB\'s Original Work...', 'info');
    
    setTimeout(() => log('[DETECT] Looking for 24-bit audio files...', 'info'), 500);
    setTimeout(() => log('[DETECT] Checking metadata chunks...', 'info'), 1500);
    setTimeout(() => log('[FOUND] 12 original files identified!', 'success'), 3000);
    
    showNotification('Finding Originals', 'Searching for 24-bit original recordings...');
}

function healWorld() {
    log('[ACTION] 🌍 HEAL THE WORLD initiated!', 'info');
    
    setTimeout(() => log('[CLEAN] Removing empty folders...', 'info'), 500);
    setTimeout(() => log('[ORGANIZE] Restructuring directories...', 'info'), 2000);
    setTimeout(() => log('[OPTIMIZE] Defragmenting indexes...', 'info'), 4000);
    setTimeout(() => log('[SUCCESS] ✅ The world is healed! GORUNFREE!!!', 'success'), 6000);
    
    showNotification('Heal The World', 'Cleaning and organizing the MC96 Universe...');
}

function refreshData() {
    log('[ACTION] Refreshing data...', 'info');
    
    renderVolumes();
    renderAlerts();
    renderOriginals();
    
    setTimeout(() => log('[SUCCESS] ✅ Data refreshed!', 'success'), 500);
    
    showNotification('Data Refreshed', 'All panels updated with latest data.');
}

function openConsole() {
    log('[ACTION] Advanced console requested', 'info');
    log('[INFO] Terminal access available via SSH', 'info');
    log('[CMD] python3 upgrade_and_consolidate.py', 'info');
    
    showNotification('Console Ready', 'Use the log panel for command output.');
}

// ========================
// Notifications
// ========================

function showNotification(title, message) {
    // Check if browser supports notifications
    if ('Notification' in window && Notification.permission === 'granted') {
        new Notification(`🌌 MC96: ${title}`, { body: message });
    }
}

// Request notification permission on load
if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission();
}

// ========================
// Keyboard Shortcuts
// ========================

document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + R = Refresh
    if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
        e.preventDefault();
        refreshData();
    }
    
    // Ctrl/Cmd + U = Upgrade
    if ((e.ctrlKey || e.metaKey) && e.key === 'u') {
        e.preventDefault();
        runUpgrade();
    }
    
    // Ctrl/Cmd + S = Scan
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        runScan();
    }
    
    // Ctrl/Cmd + H = Heal
    if ((e.ctrlKey || e.metaKey) && e.key === 'h') {
        e.preventDefault();
        healWorld();
    }
});

// ========================
// Export for external use
// ========================

window.MC96 = {
    log,
    refreshData,
    runUpgrade,
    runScan,
    findOriginals,
    healWorld,
    volumeData,
    alertsData,
    originalsData
};

console.log('🌌 MC96 Mission Control loaded successfully!');
console.log('🚀 GORUNFREE!!!');
