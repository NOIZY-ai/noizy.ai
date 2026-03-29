// CB01 Router Worker
// Classifies incoming requests and dispatches to the correct NOIZY agent.
//
// Dispatch matrix (keyword -> agent):
//   consent, verify, revoke, clearance  -> consent-gateway
//   voice, estate, royalty, hvs          -> voice-estate-agent
//   receipt, proof, audit, ledger        -> receipt-agent
//   memory, recall, context, history     -> memory-agent
//   health, ping, status                 -> direct response
//   *                                    -> default handler

export interface Env {
  CONSENT_GATEWAY_URL: string;
  VOICE_ESTATE_URL?: string;
  RECEIPT_AGENT_URL?: string;
  MEMORY_AGENT_URL?: string;
  ALLOWED_ORIGINS?: string;
}

interface DispatchResult {
  agent: string;
  url: string | null;
  direct: boolean;
}

// ---------------------------------------------------------------------------
// Keyword dispatch matrix
// ---------------------------------------------------------------------------

const DISPATCH_MATRIX: Record<string, { agent: string; envKey: keyof Env }> = {
  // Consent gateway
  consent: { agent: "consent-gateway", envKey: "CONSENT_GATEWAY_URL" },
  verify: { agent: "consent-gateway", envKey: "CONSENT_GATEWAY_URL" },
  revoke: { agent: "consent-gateway", envKey: "CONSENT_GATEWAY_URL" },
  clearance: { agent: "consent-gateway", envKey: "CONSENT_GATEWAY_URL" },
  // Voice estate agent
  voice: { agent: "voice-estate-agent", envKey: "VOICE_ESTATE_URL" },
  estate: { agent: "voice-estate-agent", envKey: "VOICE_ESTATE_URL" },
  royalty: { agent: "voice-estate-agent", envKey: "VOICE_ESTATE_URL" },
  hvs: { agent: "voice-estate-agent", envKey: "VOICE_ESTATE_URL" },
  // Receipt agent
  receipt: { agent: "receipt-agent", envKey: "RECEIPT_AGENT_URL" },
  proof: { agent: "receipt-agent", envKey: "RECEIPT_AGENT_URL" },
  audit: { agent: "receipt-agent", envKey: "RECEIPT_AGENT_URL" },
  ledger: { agent: "receipt-agent", envKey: "RECEIPT_AGENT_URL" },
  // Memory agent
  memory: { agent: "memory-agent", envKey: "MEMORY_AGENT_URL" },
  recall: { agent: "memory-agent", envKey: "MEMORY_AGENT_URL" },
  context: { agent: "memory-agent", envKey: "MEMORY_AGENT_URL" },
  history: { agent: "memory-agent", envKey: "MEMORY_AGENT_URL" },
};

const DIRECT_KEYWORDS = new Set(["health", "ping", "status"]);

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function json(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

function corsHeaders(origin: string | null, allowedOrigins: string): Record<string, string> {
  const allowed = allowedOrigins.split(",").map((o) => o.trim()).filter(Boolean);
  const effectiveOrigin =
    origin && (allowed.includes("*") || allowed.includes(origin)) ? origin : allowed[0] ?? "*";

  return {
    "Access-Control-Allow-Origin": effectiveOrigin,
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Request-ID",
    "Access-Control-Max-Age": "86400",
  };
}

function withCors(res: Response, origin: string | null, allowedOrigins: string): Response {
  const headers = new Headers(res.headers);
  for (const [k, v] of Object.entries(corsHeaders(origin, allowedOrigins))) {
    headers.set(k, v);
  }
  return new Response(res.body, { status: res.status, headers });
}

function classifyPath(path: string): DispatchResult {
  const segments = path.split("/").filter(Boolean);
  const firstSegment = segments[0]?.toLowerCase() ?? "";

  // Direct-response keywords
  if (DIRECT_KEYWORDS.has(firstSegment)) {
    return { agent: firstSegment, url: null, direct: true };
  }

  // Keyword dispatch
  const match = DISPATCH_MATRIX[firstSegment];
  if (match) {
    return { agent: match.agent, url: null, direct: false };
  }

  return { agent: "unknown", url: null, direct: false };
}

function resolveAgentUrl(dispatch: DispatchResult, env: Env, path: string): string | null {
  if (dispatch.direct) return null;

  for (const [, entry] of Object.entries(DISPATCH_MATRIX)) {
    if (entry.agent === dispatch.agent) {
      const url = env[entry.envKey];
      if (typeof url === "string" && url.length > 0) {
        // Strip the keyword prefix and forward the rest
        const segments = path.split("/").filter(Boolean);
        const rest = "/" + segments.slice(1).join("/");
        return url + rest;
      }
    }
  }

  return null;
}

// ---------------------------------------------------------------------------
// Router
// ---------------------------------------------------------------------------

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const path = url.pathname;
    const method = request.method;
    const origin = request.headers.get("Origin");
    const allowedOrigins = env.ALLOWED_ORIGINS ?? "*";

    // CORS preflight
    if (method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: corsHeaders(origin, allowedOrigins),
      });
    }

    const dispatch = classifyPath(path);
    let response: Response;

    try {
      // Direct responses
      if (dispatch.direct) {
        if (dispatch.agent === "health" || dispatch.agent === "ping") {
          response = json({
            status: "ok",
            service: "cb01-router",
            timestamp: new Date().toISOString(),
          });
        } else if (dispatch.agent === "status") {
          response = json({
            service: "cb01-router",
            agents: {
              "consent-gateway": env.CONSENT_GATEWAY_URL ? "configured" : "not configured",
              "voice-estate-agent": env.VOICE_ESTATE_URL ? "configured" : "not configured",
              "receipt-agent": env.RECEIPT_AGENT_URL ? "configured" : "not configured",
              "memory-agent": env.MEMORY_AGENT_URL ? "configured" : "not configured",
            },
            dispatch_keywords: Object.keys(DISPATCH_MATRIX),
            timestamp: new Date().toISOString(),
          });
        } else {
          response = json({ error: "Unknown direct handler" }, 500);
        }
      } else if (dispatch.agent === "unknown") {
        response = json(
          {
            error: "No agent matched for this route",
            path,
            hint: "Use a keyword prefix: consent, verify, revoke, voice, estate, receipt, memory, health, status",
          },
          404
        );
      } else {
        // Forward to agent
        const targetUrl = resolveAgentUrl(dispatch, env, path);

        if (!targetUrl) {
          response = json(
            {
              error: `Agent "${dispatch.agent}" is not configured`,
              agent: dispatch.agent,
            },
            503
          );
        } else {
          // Proxy the request
          const proxyHeaders = new Headers(request.headers);
          proxyHeaders.set("X-CB01-Agent", dispatch.agent);
          proxyHeaders.set("X-CB01-Timestamp", new Date().toISOString());

          const proxyRequest = new Request(targetUrl + url.search, {
            method: request.method,
            headers: proxyHeaders,
            body: method !== "GET" && method !== "HEAD" ? request.body : undefined,
          });

          response = await fetch(proxyRequest);
        }
      }
    } catch (err) {
      console.error("CB01 router error:", err);
      response = json(
        {
          error: "Internal routing error",
          message: err instanceof Error ? err.message : "Unknown error",
          agent: dispatch.agent,
        },
        502
      );
    }

    return withCors(response, origin, allowedOrigins);
  },
};
