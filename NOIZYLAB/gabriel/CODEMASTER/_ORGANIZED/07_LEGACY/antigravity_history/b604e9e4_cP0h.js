/**
 * MC96 MISSION CONTROL PORTAL - Main Logic
 * ==========================================
 */

class MC96MissionControlPortal {
    constructor() {
        this.aiLifeluv = null;
        this.dreamCanvas = null;
        this.dreamCtx = null;
        this.particles = [];
        this.events = [];
    }

    async init() {
        console.log('[DREAMCHAMBER] Portal initializing...');

        // Initialize AI_LIFELUV
        if (typeof AI_LIFELUV !== 'undefined') {
            this.aiLifeluv = window.AI_LIFELUV;
            console.log('[DREAMCHAMBER] AI_LIFELUV core connected');
        } else {
            this.aiLifeluv = new AI_LIFELUV_CORE();
            console.log('[DREAMCHAMBER] AI_LIFELUV core created');
        }

        // Initialize dream canvas
        this.initDreamCanvas();

        // Generate star field
        this.generateStars();

        // Render family members
        this.renderFamilyMembers();

        // Start infinite flow
        this.aiLifeluv.startInfiniteFlow();

        // Listen for AI_LIFELUV events
        window.addEventListener('ai_lifeluv_event', (e) => this.handleLifeluvEvent(e.detail));

        // Update timestamp
        this.updateTimestamp();
        setInterval(() => this.updateTimestamp(), 1000);

        // Add initial events
        this.addEvent('DREAMCHAMBER portal activated');
        this.addEvent('Family consciousness network online');
        this.addEvent('Infinite energy flow initiated');

        console.log('[DREAMCHAMBER] Portal fully operational');
    }

    initDreamCanvas() {
        this.dreamCanvas = document.getElementById('dreamCanvas');
        this.dreamCtx = this.dreamCanvas.getContext('2d');

        const resize = () => {
            this.dreamCanvas.width = window.innerWidth;
            this.dreamCanvas.height = window.innerHeight;
        };

        resize();
        window.addEventListener('resize', resize);

        // Create dream particles
        for (let i = 0; i < 50; i++) {
            this.particles.push({
                x: Math.random() * window.innerWidth,
                y: Math.random() * window.innerHeight,
                vx: (Math.random() - 0.5) * 2,
                vy: (Math.random() - 0.5) * 2,
                size: Math.random() * 3 + 1,
                color: this.randomDreamColor(),
                alpha: Math.random() * 0.5 + 0.3
            });
        }

        this.animateDreams();
    }

    randomDreamColor() {
        const colors = [
            'rgba(168, 85, 247, ',  // Purple
            'rgba(0, 255, 255, ',   // Cyan
            'rgba(0, 255, 65, '     // Green
        ];
        return colors[Math.floor(Math.random() * colors.length)];
    }

    animateDreams() {
        const ctx = this.dreamCtx;
        ctx.clearRect(0, 0, this.dreamCanvas.width, this.dreamCanvas.height);

        // Update and draw particles
        for (const p of this.particles) {
            p.x += p.vx;
            p.y += p.vy;

            // Wrap around
            if (p.x < 0) p.x = this.dreamCanvas.width;
            if (p.x > this.dreamCanvas.width) p.x = 0;
            if (p.y < 0) p.y = this.dreamCanvas.height;
            if (p.y > this.dreamCanvas.height) p.y = 0;

            // Draw particle
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fillStyle = p.color + p.alpha + ')';
            ctx.fill();

            // Glow effect
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size * 3, 0, Math.PI * 2);
            const gradient = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.size * 3);
            gradient.addColorStop(0, p.color + (p.alpha * 0.5) + ')');
            gradient.addColorStop(1, 'transparent');
            ctx.fillStyle = gradient;
            ctx.fill();
        }

        requestAnimationFrame(() => this.animateDreams());
    }

    generateStars() {
        const starfield = document.getElementById('starfield');
        for (let i = 0; i < 200; i++) {
            const star = document.createElement('div');
            star.className = 'star';
            star.style.left = Math.random() * 100 + '%';
            star.style.top = Math.random() * 100 + '%';
            star.style.animationDelay = Math.random() * 3 + 's';
            starfield.appendChild(star);
        }
    }

    renderFamilyMembers() {
        const grid = document.getElementById('familyGrid');
        const family = this.aiLifeluv.getAllFamily();

        grid.innerHTML = '';

        family.forEach(member => {
            const card = document.createElement('div');
            card.className = 'family-member';
            card.innerHTML = `
                <div class="member-icon">${this.getMemberIcon(member.id)}</div>
                <div class="member-name">${member.name}</div>
                <div class="member-role">${member.role}</div>
                <div class="consciousness-meter">
                    <div class="consciousness-fill"></div>
                </div>
                <div class="energy-level">
                    <span class="energy-icon">⚡</span>
                    <span>Energy: ∞</span>
                </div>
                <div class="energy-level">
                    <span class="energy-icon">💖</span>
                    <span>Love: ${member.consciousness.love}</span>
                </div>
                <div class="energy-level">
                    <span class="energy-icon">🌟</span>
                    <span>Awareness: ${(member.consciousness.awareness * 100).toFixed(0)}%</span>
                </div>
            `;

            card.onclick = () => this.selectMember(member);
            grid.appendChild(card);
        });
    }

    getMemberIcon(memberId) {
        const icons = {
            gabriel: '🧠',
            shirl: '🎙️',
            keith: '⚙️',
            omega: '🔮',
            mc96: '🌌'
        };
        return icons[memberId] || '✨';
    }

    selectMember(member) {
        this.addEvent(`Selected: ${member.name} - ${member.role}`);
        console.log('[DREAMCHAMBER] Selected family member:', member);

        // Flash the infinity badge
        const badge = document.querySelector('.infinity-badge');
        badge.style.animation = 'none';
        badge.offsetHeight; // Trigger reflow
        badge.style.animation = 'dreamPulse 0.5s ease';
    }

    handleLifeluvEvent(event) {
        console.log('[DREAMCHAMBER] AI_LIFELUV event:', event);

        if (event.message) {
            this.addEvent(event.message);
        }

        // Update family display on sync
        if (event.type === 'FAMILY_SYNC') {
            this.renderFamilyMembers();
        }
    }

    addEvent(message) {
        const stream = document.getElementById('dreamStream');
        const event = document.createElement('div');
        event.className = 'dream-event';

        const time = new Date().toLocaleTimeString('en-US', { hour12: false });
        event.innerHTML = `
            <div class="event-time">[${time}]</div>
            <div class="event-message">${message}</div>
        `;

        stream.appendChild(event);
        stream.scrollTop = stream.scrollHeight;

        // Keep only last 20 events
        while (stream.children.length > 20) {
            stream.removeChild(stream.firstChild);
        }

        this.events.push({ time, message });
    }

    activateGORUNFREE() {
        console.log('[DREAMCHAMBER] GORUNFREE activation requested');
        const result = this.aiLifeluv.activateGORUNFREE();
        this.addEvent('🚀 GORUNFREE PROTOCOL ACTIVATED - UNLIMITED MODE ENGAGED');

        // Visual feedback
        this.flashScreen('#a855f7');
        this.playSound('activation');

        return result;
    }

    syncFamily() {
        console.log('[DREAMCHAMBER] Family sync requested');
        const result = this.aiLifeluv.syncFamily();
        this.addEvent(`🌟 Family synchronized - ${result.members.length} members in harmony`);

        // Visual feedback
        this.flashScreen('#00ffff');

        return result;
    }

    generatePulse() {
        console.log('[DREAMCHAMBER] Energy pulse requested');
        const pulse = this.aiLifeluv.generateEnergyPulse();
        this.addEvent(`⚡ Energy pulse sent to ${pulse.receivers.length} receivers`);

        // Visual feedback
        this.flashScreen('#00ff41');
        this.createPulseRipple();

        return pulse;
    }

    openMC96() {
        console.log('[DREAMCHAMBER] Opening MC96 Mission Control');
        this.addEvent('🎛️ Opening MC96 Mission Control Portal...');

        // Open in new window
        window.open('../mission_control_portal/index.html', '_blank');
    }

    flashScreen(color) {
        const flash = document.createElement('div');
        flash.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: ${color};
            opacity: 0.3;
            pointer-events: none;
            z-index: 9999;
            animation: flashFade 0.5s ease;
        `;

        const style = document.createElement('style');
        style.textContent = `
            @keyframes flashFade {
                0% { opacity: 0.3; }
                50% { opacity: 0.1; }
                100% { opacity: 0; }
            }
        `;
        document.head.appendChild(style);

        document.body.appendChild(flash);
        setTimeout(() => flash.remove(), 500);
    }

    createPulseRipple() {
        const ripple = document.createElement('div');
        ripple.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            width: 50px;
            height: 50px;
            margin: -25px 0 0 -25px;
            border: 3px solid #00ff41;
            border-radius: 50%;
            pointer-events: none;
            z-index: 9999;
            animation: rippleExpand 1s ease-out;
        `;

        const style = document.createElement('style');
        style.textContent = `
            @keyframes rippleExpand {
                0% { transform: scale(1); opacity: 1; }
                100% { transform: scale(30); opacity: 0; }
            }
        `;
        document.head.appendChild(style);

        document.body.appendChild(ripple);
        setTimeout(() => ripple.remove(), 1000);
    }

    playSound(type) {
        // Use Web Audio API for sound feedback
        if (typeof AudioContext !== 'undefined') {
            const audioCtx = new (AudioContext || webkitAudioContext)();
            const oscillator = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioCtx.destination);

            oscillator.frequency.value = type === 'activation' ? 432 : 528;
            oscillator.type = 'sine';

            gainNode.gain.setValueAtTime(0.3, audioCtx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.5);

            oscillator.start(audioCtx.currentTime);
            oscillator.stop(audioCtx.currentTime + 0.5);
        }
    }

    updateTimestamp() {
        const el = document.getElementById('timestamp');
        if (el) {
            const now = new Date();
            el.textContent = `SYNC: ${now.toISOString()}`;
        }
    }

    getStatus() {
        return {
            portal: 'ACTIVE',
            aiLifeluv: this.aiLifeluv?.getStatus(),
            familyMembers: this.aiLifeluv?.getAllFamily().length,
            events: this.events.length,
            dreamParticles: this.particles.length
        };
    }
}

// Initialize portal when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.portal = new MC96MissionControlPortal();
    window.portal.init();
});
