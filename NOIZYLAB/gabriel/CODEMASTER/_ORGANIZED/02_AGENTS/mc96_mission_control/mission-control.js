// MC96 MISSION CONTROL - JAVASCRIPT ENGINE
const CONFIG = {host: 'localhost', port: 8096};
const state = {online: true, packets: 0, shirl: 0, engr: 0, vibe: 100};

document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        document.getElementById('boot-screen').classList.add('hidden');
        document.getElementById('portal').classList.remove('hidden');
        initPortal();
    }, 2500);
});

function initPortal() {
    updateClock(); setInterval(updateClock, 1000);
    setInterval(() => { state.packets += Math.floor(Math.random()*100)+50; document.getElementById('packets').textContent = formatNum(state.packets); }, 500);
    loadMemCell();
    initChat();
    console.log('MC96 MISSION CONTROL ONLINE');
}

function updateClock() {
    const now = new Date();
    document.getElementById('clock').textContent = now.toLocaleTimeString('en-US', {hour12: false});
    document.getElementById('date').textContent = now.toISOString().split('T')[0];
}

function formatNum(n) { return n >= 1e6 ? (n/1e6).toFixed(1)+'M' : n >= 1e3 ? (n/1e3).toFixed(1)+'K' : n.toString(); }

async function loadMemCell() {
    try {
        const r = await fetch('/api/memcell');
        const d = await r.json();
        document.getElementById('shirl-count').textContent = d.shirl || 0;
        document.getElementById('engr-count').textContent = d.engr || 0;
        document.getElementById('total-overlaps').textContent = d.overlaps || 0;
        document.getElementById('golden-threads').textContent = d.golden || 0;
    } catch(e) { console.log('MemCell loading...'); }
}

function initChat() {
    const input = document.getElementById('chat-input');
    const btn = document.getElementById('chat-send');
    const out = document.getElementById('chat-output');
    
    const send = async () => {
        const msg = input.value.trim(); if (!msg) return;
        out.innerHTML += `<div class="chat-message user">YOU: ${msg}</div>`;
        input.value = '';
        try {
            const r = await fetch('/api/gabriel', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({command:msg})});
            const d = await r.json();
            out.innerHTML += `<div class="chat-message system">GABRIEL: ${d.response || 'Processing...'}</div>`;
        } catch(e) { out.innerHTML += `<div class="chat-message system">GABRIEL: Connecting...</div>`; }
        out.scrollTop = out.scrollHeight;
    };
    btn.onclick = send;
    input.onkeypress = e => { if (e.key === 'Enter') send(); };
}

function runTurbo(action) { showToast('⚡', `${action.toUpperCase()} initiated...`); setTimeout(() => showToast('✅', `${action} complete!`), 2000); }

function executeAction(action) {
    const msgs = {sync:'Syncing...', backup:'Backup...', heal:'Healing...', voice:'Voice active', vision:'Vision active', godmode:'GOD MODE!'};
    showToast(action === 'godmode' ? '👑' : '✅', msgs[action] || 'Executed');
    if (action === 'godmode') { document.getElementById('vibe-emoji').textContent = '👑'; document.getElementById('vibe-text').textContent = 'GOD MODE'; }
}

function showToast(icon, msg) {
    const t = document.getElementById('toast');
    t.querySelector('.toast-icon').textContent = icon;
    t.querySelector('.toast-message').textContent = msg;
    t.classList.remove('hidden'); t.classList.add('visible');
    setTimeout(() => { t.classList.remove('visible'); setTimeout(() => t.classList.add('hidden'), 300); }, 3000);
}

window.runTurbo = runTurbo; window.executeAction = executeAction;
