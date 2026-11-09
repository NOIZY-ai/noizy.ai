/**
 * MC96 Command Center
 * Serves the dashboard for GOD and GABRIEL tunnels.
 */

export default {
  async fetch(request, env, ctx) {
    const html = `
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MC96 Command Center</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f0f0f; color: #fff; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }
            .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; max-width: 800px; width: 100%; }
            .card { background: #1a1a1a; padding: 20px; border-radius: 12px; text-decoration: none; color: inherit; transition: transform 0.2s, background 0.2s; border: 1px solid #333; }
            .card:hover { transform: translateY(-5px); background: #252525; border-color: #00ff88; }
            h1 { margin-bottom: 40px; font-weight: 800; letter-spacing: -1px; background: linear-gradient(45deg, #00ff88, #00b8ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
            h2 { margin: 0 0 10px 0; font-size: 1.5rem; }
            .status { font-size: 0.9rem; color: #888; display: flex; align-items: center; gap: 8px; }
            .dot { width: 8px; height: 8px; background: #444; border-radius: 50%; }
            .dot.online { background: #00ff88; box-shadow: 0 0 10px #00ff88; }
        </style>
    </head>
    <body>
        <h1>MC96 COMMAND CENTER</h1>
        <div class="grid">
            <a href="https://vscode.dev/tunnel/GOD" class="card" target="_blank">
                <h2>GOD (Mac)</h2>
                <div class="status"><span class="dot online"></span> Mac Studio M2 Ultra</div>
            </a>
            <a href="https://vscode.dev/tunnel/GABRIEL" class="card" target="_blank">
                <h2>GABRIEL (Win)</h2>
                <div class="status"><span class="dot online"></span> PC / Windows 11</div>
            </a>
            <a href="https://switch.fishmusicinc.com" class="card" target="_blank">
                <h2>SWITCH</h2>
                <div class="status"><span class="dot"></span> DGS-1210-10</div>
            </a>
            <a href="/api/status" class="card">
                <h2>SYSTEM HEALTH</h2>
                <div class="status"><span class="dot"></span> Monitoring Port 9999</div>
            </a>
        </div>
    </body>
    </html>
    `;

    if (new URL(request.url).pathname === "/api/status") {
       return new Response(JSON.stringify({ status: "ok", time: new Date().toISOString() }), {
           headers: { "Content-Type": "application/json" }
       });
    }

    return new Response(html, {
      headers: { "content-type": "text/html;charset=UTF-8" },
    });
  },
};
