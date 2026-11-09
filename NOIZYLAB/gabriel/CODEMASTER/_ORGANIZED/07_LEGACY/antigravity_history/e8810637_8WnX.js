/**
 * NEURAL ENGINE 1.0 (Canvas Force-Graph)
 * ======================================
 * Renders the MemCell Brain in real-time.
 * GORUNFREE!!!
 */

const NeuralConfig = {
     particleColor: '#00ff9d',
     lineColor: 'rgba(124, 58, 237, 0.2)',
     nodeSize: 4,
     interactionRadius: 100,
     physics: {
          repulsion: 100,
          springLength: 80,
          springK: 0.05,
          damping: 0.9
     }
};

class NeuralEngine {
     constructor(canvasId) {
          this.canvas = document.getElementById(canvasId);
          if (!this.canvas) return;

          this.ctx = this.canvas.getContext('2d');
          this.nodes = [];
          this.links = [];
          this.width = this.canvas.offsetWidth;
          this.height = this.canvas.offsetHeight;

          // Resize Handler
          window.addEventListener('resize', () => this.resize());
          this.resize();

          // Mouse Interaction
          this.mouse = { x: -1000, y: -1000 };
          this.canvas.addEventListener('mousemove', (e) => {
               const rect = this.canvas.getBoundingClientRect();
               this.mouse.x = e.clientX - rect.left;
               this.mouse.y = e.clientY - rect.top;
          });

          // Start Loop
          this.animate = this.animate.bind(this);
          requestAnimationFrame(this.animate);

          // Initial Fetch
          this.fetchBrain();
          // Polling
          setInterval(() => this.fetchBrain(), 5000);
     }

     resize() {
          this.canvas.width = this.canvas.parentElement.offsetWidth;
          this.canvas.height = this.canvas.parentElement.offsetHeight || 300;
          this.width = this.canvas.width;
          this.height = this.canvas.height;
     }

     async fetchBrain() {
          try {
               // Using the new Port 5174
               const response = await fetch('http://localhost:5174/api/memcell/graph');
               const data = await response.json();
               this.updateGraph(data);
          } catch (e) {
               console.error("Brain Connection Lost:", e);
          }
     }

     updateGraph(data) {
          // Merge nodes (keep positions if existing)
          const newNodes = [];
          data.nodes.forEach(n => {
               const existing = this.nodes.find(en => en.id === n.id);
               if (existing) {
                    // Update val/meta but keep x/y/vx/vy
                    existing.val = n.val;
                    newNodes.push(existing);
               } else {
                    // Spawn new
                    newNodes.push({
                         id: n.id,
                         label: n.label,
                         x: Math.random() * this.width,
                         y: Math.random() * this.height,
                         vx: (Math.random() - 0.5) * 2,
                         vy: (Math.random() - 0.5) * 2,
                         val: n.val || 1,
                         category: n.category
                    });
               }
          });
          this.nodes = newNodes;

          // Links are simple replacement for now (or could track them too)
          // We need to map source/target IDs to node objects references for physics
          this.links = data.links.map(l => ({
               source: this.nodes.find(n => n.id === l.source),
               target: this.nodes.find(n => n.id === l.target),
               strength: l.strength || 0.1
          })).filter(l => l.source && l.target);
     }

     applyPhysics() {
          // 1. Repulsion (All nodes repel)
          for (let i = 0; i < this.nodes.length; i++) {
               for (let j = i + 1; j < this.nodes.length; j++) {
                    const a = this.nodes[i];
                    const b = this.nodes[j];
                    const dx = a.x - b.x;
                    const dy = a.y - b.y;
                    const distSq = dx * dx + dy * dy + 0.1;
                    const force = NeuralConfig.physics.repulsion / distSq;

                    const fx = (dx / Math.sqrt(distSq)) * force;
                    const fy = (dy / Math.sqrt(distSq)) * force;

                    a.vx += fx;
                    a.vy += fy;
                    b.vx -= fx;
                    b.vy -= fy;
               }
          }

          // 2. Attraction (Links pull)
          this.links.forEach(link => {
               const dx = link.target.x - link.source.x;
               const dy = link.target.y - link.source.y;
               const dist = Math.sqrt(dx * dx + dy * dy);
               const force = (dist - NeuralConfig.physics.springLength) * NeuralConfig.physics.springK;

               const fx = (dx / dist) * force;
               const fy = (dy / dist) * force;

               link.source.vx += fx;
               link.source.vy += fy;
               link.target.vx -= fx;
               link.target.vy -= fy;
          });

          // 3. Center Gravity (Keep in view)
          const cx = this.width / 2;
          const cy = this.height / 2;
          this.nodes.forEach(n => {
               n.vx += (cx - n.x) * 0.0005;
               n.vy += (cy - n.y) * 0.0005;

               // Damping
               n.vx *= NeuralConfig.physics.damping;
               n.vy *= NeuralConfig.physics.damping;

               // Move
               n.x += n.vx;
               n.y += n.vy;

               // Mouse Interaction (Push away)
               const mdx = n.x - this.mouse.x;
               const mdy = n.y - this.mouse.y;
               const mdist = Math.sqrt(mdx * mdx + mdy * mdy);
               if (mdist < 100) {
                    n.vx += (mdx / mdist) * 2;
                    n.vy += (mdy / mdist) * 2;
               }
          });
     }

     draw() {
          this.ctx.clearRect(0, 0, this.width, this.height);

          // Draw Links
          this.ctx.strokeStyle = NeuralConfig.lineColor;
          this.ctx.beginPath();
          this.links.forEach(l => {
               this.ctx.moveTo(l.source.x, l.source.y);
               this.ctx.lineTo(l.target.x, l.target.y);
          });
          this.ctx.stroke();

          // Draw Nodes
          this.nodes.forEach(n => {
               this.ctx.beginPath();
               const radius = NeuralConfig.nodeSize + (n.val * 0.5); // Size based on access count
               this.ctx.arc(n.x, n.y, radius, 0, Math.PI * 2);

               // Color based on category attempt
               this.ctx.fillStyle = NeuralConfig.particleColor;
               if (n.category === 'context') this.ctx.fillStyle = '#00d4ff'; // Blue
               if (n.category === 'code') this.ctx.fillStyle = '#f59e0b'; // Orange
               if (n.category === 'execution') this.ctx.fillStyle = '#ef4444'; // Red

               this.ctx.shadowBlur = 10;
               this.ctx.shadowColor = this.ctx.fillStyle;
               this.ctx.fill();
               this.ctx.shadowBlur = 0;

               // Label on Hover (approx)
               const mdx = n.x - this.mouse.x;
               const mdy = n.y - this.mouse.y;
               const mdist = Math.sqrt(mdx * mdx + mdy * mdy);
               if (mdist < 20) {
                    this.ctx.fillStyle = '#fff';
                    this.ctx.font = '10px Rajdhani';
                    this.ctx.fillText(n.label, n.x + 10, n.y);
               }
          });
     }

     animate() {
          this.applyPhysics();
          this.draw();
          requestAnimationFrame(this.animate);
     }
}

// Init when DOM Ready
document.addEventListener('DOMContentLoaded', () => {
     // Look for canvas
     const canvas = document.getElementById('neural-canvas');
     if (canvas) {
          window.neuralEngine = new NeuralEngine('neural-canvas');
     }
});
