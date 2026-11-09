// cloudflare_worker.js
// NOIZY.ai EDGE LOGIC
// Deployed to: noizy-ai.workers.dev

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // "Hot Rod" Header Injection
    const headers = new Headers({
      'X-Powered-By': 'NOIZY-EDGE-NETWORK',
      'X-Latency': '0ms',
      'X-Admin': 'rsplowman@icloud.com',
      'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload'
    });

    // Handle Email Webhooks (Simulated)
    if (url.pathname === '/email-webhook') {
      return new Response("Routing to rsplowman@icloud.com confirmed.", { status: 200, headers });
    }

    // Serve App
    return new Response("NOIZY.ai Systems Online. Cloudflare Protection Active.", {
      headers: headers
    });
  }
};
