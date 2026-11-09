// library.js
// THE INFINITE CRATE: Visual Audio Browser

class AudioLibrary {
    constructor() {
        this.manifest = null;
        this.container = document.getElementById('library-list');
        this.searchInput = document.getElementById('library-search');
        this.countDisplay = document.getElementById('library-count');
        
        if (!this.container) return;
        
        // Event Listeners
        this.searchInput.addEventListener('input', (e) => this.filter(e.target.value));
        
        // Boot
        this.init();
    }

    async init() {
        // Listen for the engine to load the manifest first, or fetch it ourselves
        window.addEventListener('noizy-manifest-loaded', (e) => {
            this.manifest = e.detail;
            this.render(this.manifest.assets);
        });
        
        // Fallback or Direct Load check
        if (window.AudioSys && window.AudioSys.audioManifest) {
            this.manifest = window.AudioSys.audioManifest;
            this.render(this.manifest.assets);
        }
    }

    render(assets) {
        if (!this.container) return;
        this.container.innerHTML = '';
        
        // Virtualize? For now, render first 100 for speed, then lazy load
        // Actually, let's just render the top 100 matches to keep DOM light
        const subset = assets.slice(0, 100);
        
        subset.forEach(asset => {
            const el = document.createElement('div');
            el.className = 'lib-item';
            el.innerHTML = `
                <div class="lib-icon">🎵</div>
                <div class="lib-info">
                    <div class="lib-name">${asset.name}</div>
                    <div class="lib-path">${this.formatPath(asset.source)}</div>
                </div>
                <div class="lib-action">▶</div>
            `;
            
            el.addEventListener('click', () => {
                this.play(asset);
                // Highlight active
                document.querySelectorAll('.lib-item').forEach(i => i.classList.remove('active'));
                el.classList.add('active');
            });
            
            this.container.appendChild(el);
        });
        
        // Update Count
        if (this.countDisplay) {
            this.countDisplay.textContent = `${assets.length} ASSETS FOUND`;
        }
    }

    filter(query) {
        if (!this.manifest) return;
        
        const term = query.toLowerCase();
        const results = this.manifest.assets.filter(a => 
            a.name.toLowerCase().includes(term) || 
            a.source.toLowerCase().includes(term)
        );
        
        this.render(results);
    }
    
    play(asset) {
        if (window.AudioSys) {
            // Because of browser security, we might need to handle local file paths carefully.
            // If the manifest paths are absolute local paths, standard fetch might fail unless served correctly.
            // For this demo environment, we assume the server can serve them or we try relative.
            console.log("LIBRARY // REQUESTING PLAY:", asset.path);
            window.AudioSys.playSample(asset.path);
        }
    }
    
    formatPath(path) {
        // Shorten path for display: /Volumes/SAMPLE_MASTER -> [SAMPLE_MASTER]
        return path.replace('/Volumes/', '[').replace('/', '] ').replace('/Users/m2ultra/.gemini/antigravity/scratch/', '[LOCAL] ');
    }
}

// Initialize on Load
window.addEventListener('DOMContentLoaded', () => {
    window.Library = new AudioLibrary();
});
