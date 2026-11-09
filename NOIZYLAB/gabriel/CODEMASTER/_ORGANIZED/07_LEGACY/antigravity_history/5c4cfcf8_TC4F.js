/**
 * AUDIO REACTIVE AVATAR ENGINE
 * Canvas-based visualization for "Living Brain" effect
 */

class AvatarEngine {
     constructor(canvasId) {
          this.canvas = document.getElementById(canvasId);
          if (!this.canvas) return;

          this.ctx = this.canvas.getContext('2d');
          this.particles = [];
          this.width = 0;
          this.height = 0;
          this.color = '#7c3aed'; // Purple base
          this.active = true;

          this.resize();
          window.addEventListener('resize', () => this.resize());

          this.initParticles(50);
          this.animate();
     }

     resize() {
          // Parent container dimensions
          const rect = this.canvas.parentElement.getBoundingClientRect();
          this.width = rect.width;
          this.height = rect.height;
          this.canvas.width = this.width;
          this.canvas.height = this.height;
     }

     initParticles(count) {
          for (let i = 0; i < count; i++) {
               this.particles.push({
                    x: Math.random() * this.width,
                    y: Math.random() * this.height,
                    vx: (Math.random() - 0.5) * 2,
                    vy: (Math.random() - 0.5) * 2,
                    size: Math.random() * 3 + 1,
                    life: Math.random()
               });
          }
     }

     triggerHealEffect() {
          this.color = '#10b981'; // Green for heal
          // Explode particles
          this.particles.forEach(p => {
               p.vx *= 5;
               p.vy *= 5;
          });
          setTimeout(() => this.color = '#7c3aed', 3000);
     }

     triggerScanEffect() {
          this.color = '#00d4ff'; // Cyan for scan
          setTimeout(() => this.color = '#7c3aed', 2000);
     }

     draw() {
          this.ctx.fillStyle = 'rgba(10, 10, 15, 0.2)'; // Trail effect
          this.ctx.fillRect(0, 0, this.width, this.height);

          this.ctx.strokeStyle = this.color;
          this.ctx.fillStyle = this.color;

          // Update and draw particles
          this.particles.forEach((p, index) => {
               p.x += p.vx;
               p.y += p.vy;

               // Bounce
               if (p.x < 0 || p.x > this.width) p.vx *= -1;
               if (p.y < 0 || p.y > this.height) p.vy *= -1;

               // Draw
               this.ctx.beginPath();
               this.ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
               this.ctx.fill();

               // Connect near particles
               for (let j = index + 1; j < this.particles.length; j++) {
                    const p2 = this.particles[j];
                    const dx = p.x - p2.x;
                    const dy = p.y - p2.y;
                    const dist = Math.sqrt(dx * dx + dy * dy);

                    if (dist < 100) {
                         this.ctx.lineWidth = (100 - dist) / 500;
                         this.ctx.beginPath();
                         this.ctx.moveTo(p.x, p.y);
                         this.ctx.lineTo(p2.x, p2.y);
                         this.ctx.stroke();
                    }
               }
          });
     }

     animate() {
          if (!this.active) return;
          this.draw();
          requestAnimationFrame(() => this.animate());
     }
}

// Auto-init if canvas exists
window.addEventListener('DOMContentLoaded', () => {
     if (document.getElementById('avatar-canvas')) {
          window.avatar = new AvatarEngine('avatar-canvas');
     }
});
