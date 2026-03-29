// NOIZY Consent Gateway v1.0
// Enforces consent-as-code at the edge.
// Every request to use a creator's voice/asset must pass through this gateway.
//
// Pipeline:
// 1. Creator verification (HVS record in KV)
// 2. Consent record lookup (D1)
// 3. Scope exclusion check
// 4. Clearance token generation
// 5. Usage event logging (D1)
// 6. Receipt routing (triggers receipt generation)

export interface Env {
  CONSENT_KV: KVNamespace;
  AGENT_MEMORY: D1Database;
  GATEWAY_VERSION?: string;
  ALLOWED_ORIGINS?: string;
}

interface VerifyRequest {
  creator_id: string;
  usage_type: string;
  asset_ref: string;
  requestor_id: string;
}

interface RevokeRequest {
  creator_id: string;
  consent_id: string;
}

interface ConsentRecord {
  id: string;
  creator_id: string;
  consent_id: string;
  status: "active" | "revoked";
  scope_json: string;
  usage_types: string;
  exclusions: string;
  granted_at: string;
  revoked_at: string | null;
  created_at: string;
}

interface VoiceEstate {
  id: string;
  creator_id: string;
  display_name: string;
  hvs_hash: string;
  estate_status: "active" | "frozen" | "legacy";
  royalty_rule: string;
  created_at: string;
  updated_at: string;
}

type ClearanceResult = {
  status: "cleared" | "blocked";
  clearance_token: string | null;
  reason: string;
  creator_id: string;
  usage_type: string;
  consent_id: string | null;
  royalty_rule: string | null;
  timestamp: string;
};

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const VERSION = "1.0.0";

function json(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

function corsHeaders(origin: string | null, allowedOrigins: string): Record<string, string> {
  const allowed = allowedOrigins
    .split(",")
    .map((o) => o.trim())
    .filter(Boolean);

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

function generateToken(): string {
  const bytes = new Uint8Array(24);
  crypto.getRandomValues(bytes);
  return Array.from(bytes)
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

function nowISO(): string {
  return new Date().toISOString();
}

// ---------------------------------------------------------------------------
// Route handlers
// ---------------------------------------------------------------------------

async function handleVerify(request: Request, env: Env): Promise<Response> {
  let body: VerifyRequest;
  try {
    body = await request.json();
  } catch {
    return json({ error: "Invalid JSON body" }, 400);
  }

  const { creator_id, usage_type, asset_ref, requestor_id } = body;

  if (!creator_id || !usage_type || !asset_ref || !requestor_id) {
    return json({ error: "Missing required fields: creator_id, usage_type, asset_ref, requestor_id" }, 400);
  }

  const timestamp = nowISO();

  // ------------------------------------------------------------------
  // Step 1 — Creator verification via KV (HVS record)
  // ------------------------------------------------------------------
  const hvsRaw = await env.CONSENT_KV.get(`hvs:${creator_id}`);
  if (!hvsRaw) {
    await logEvent(env, {
      creator_id,
      consent_id: null,
      event_type: "block",
      usage_type,
      asset_ref,
      requestor_id,
      result: "blocked",
      reason: "creator_not_found",
      clearance_token: null,
    });

    return json({
      status: "blocked",
      clearance_token: null,
      reason: "Creator not found in HVS registry",
      creator_id,
      usage_type,
      consent_id: null,
      royalty_rule: null,
      timestamp,
    } satisfies ClearanceResult);
  }

  // ------------------------------------------------------------------
  // Step 2 — Voice estate lookup
  // ------------------------------------------------------------------
  const estate = await env.AGENT_MEMORY.prepare(
    "SELECT * FROM voice_estate WHERE creator_id = ? AND estate_status = 'active' LIMIT 1"
  )
    .bind(creator_id)
    .first<VoiceEstate>();

  if (!estate) {
    await logEvent(env, {
      creator_id,
      consent_id: null,
      event_type: "block",
      usage_type,
      asset_ref,
      requestor_id,
      result: "blocked",
      reason: "estate_inactive",
      clearance_token: null,
    });

    return json({
      status: "blocked",
      clearance_token: null,
      reason: "Creator voice estate is not active",
      creator_id,
      usage_type,
      consent_id: null,
      royalty_rule: null,
      timestamp,
    } satisfies ClearanceResult);
  }

  // ------------------------------------------------------------------
  // Step 3 — Consent record lookup (D1)
  // ------------------------------------------------------------------
  const consent = await env.AGENT_MEMORY.prepare(
    "SELECT * FROM consent_records WHERE creator_id = ? AND status = 'active' ORDER BY granted_at DESC LIMIT 1"
  )
    .bind(creator_id)
    .first<ConsentRecord>();

  if (!consent) {
    await logEvent(env, {
      creator_id,
      consent_id: null,
      event_type: "block",
      usage_type,
      asset_ref,
      requestor_id,
      result: "blocked",
      reason: "no_active_consent",
      clearance_token: null,
    });

    return json({
      status: "blocked",
      clearance_token: null,
      reason: "No active consent record for this creator",
      creator_id,
      usage_type,
      consent_id: null,
      royalty_rule: estate.royalty_rule,
      timestamp,
    } satisfies ClearanceResult);
  }

  // ------------------------------------------------------------------
  // Step 4 — Scope & exclusion check
  // ------------------------------------------------------------------
  const allowedTypes = consent.usage_types
    ? consent.usage_types.split(",").map((t) => t.trim())
    : [];

  if (allowedTypes.length > 0 && !allowedTypes.includes(usage_type) && !allowedTypes.includes("*")) {
    await logEvent(env, {
      creator_id,
      consent_id: consent.consent_id,
      event_type: "block",
      usage_type,
      asset_ref,
      requestor_id,
      result: "blocked",
      reason: "usage_type_not_permitted",
      clearance_token: null,
    });

    return json({
      status: "blocked",
      clearance_token: null,
      reason: `Usage type "${usage_type}" is not covered by active consent`,
      creator_id,
      usage_type,
      consent_id: consent.consent_id,
      royalty_rule: estate.royalty_rule,
      timestamp,
    } satisfies ClearanceResult);
  }

  // Check exclusions
  if (consent.exclusions) {
    let exclusions: string[] = [];
    try {
      exclusions = JSON.parse(consent.exclusions);
    } catch {
      exclusions = consent.exclusions.split(",").map((e) => e.trim());
    }

    if (exclusions.includes(requestor_id) || exclusions.includes(usage_type)) {
      await logEvent(env, {
        creator_id,
        consent_id: consent.consent_id,
        event_type: "block",
        usage_type,
        asset_ref,
        requestor_id,
        result: "blocked",
        reason: "excluded_by_creator",
        clearance_token: null,
      });

      return json({
        status: "blocked",
        clearance_token: null,
        reason: "Request is excluded by creator consent rules",
        creator_id,
        usage_type,
        consent_id: consent.consent_id,
        royalty_rule: estate.royalty_rule,
        timestamp,
      } satisfies ClearanceResult);
    }
  }

  // ------------------------------------------------------------------
  // Step 5 — Clearance token generation
  // ------------------------------------------------------------------
  const clearanceToken = `clr_${generateToken()}`;

  // ------------------------------------------------------------------
  // Step 6 — Log the clearance event
  // ------------------------------------------------------------------
  await logEvent(env, {
    creator_id,
    consent_id: consent.consent_id,
    event_type: "verify",
    usage_type,
    asset_ref,
    requestor_id,
    result: "cleared",
    reason: "consent_verified",
    clearance_token: clearanceToken,
  });

  // Cache clearance in KV for fast subsequent lookups (TTL 5 min)
  await env.CONSENT_KV.put(
    `clearance:${clearanceToken}`,
    JSON.stringify({ creator_id, consent_id: consent.consent_id, usage_type, asset_ref, requestor_id, timestamp }),
    { expirationTtl: 300 }
  );

  return json({
    status: "cleared",
    clearance_token: clearanceToken,
    reason: "Consent verified — usage approved",
    creator_id,
    usage_type,
    consent_id: consent.consent_id,
    royalty_rule: estate.royalty_rule,
    timestamp,
  } satisfies ClearanceResult);
}

async function handleRevoke(request: Request, env: Env): Promise<Response> {
  let body: RevokeRequest;
  try {
    body = await request.json();
  } catch {
    return json({ error: "Invalid JSON body" }, 400);
  }

  const { creator_id, consent_id } = body;

  if (!creator_id || !consent_id) {
    return json({ error: "Missing required fields: creator_id, consent_id" }, 400);
  }

  const now = nowISO();

  // Revoke in D1
  const result = await env.AGENT_MEMORY.prepare(
    "UPDATE consent_records SET status = 'revoked', revoked_at = ? WHERE creator_id = ? AND consent_id = ? AND status = 'active'"
  )
    .bind(now, creator_id, consent_id)
    .run();

  if (!result.meta.changes || result.meta.changes === 0) {
    return json({ error: "No active consent record found matching the provided creator_id and consent_id" }, 404);
  }

  // Purge related KV entries
  await env.CONSENT_KV.delete(`consent:${creator_id}:${consent_id}`);

  // Log revocation event
  await logEvent(env, {
    creator_id,
    consent_id,
    event_type: "revoke",
    usage_type: null,
    asset_ref: null,
    requestor_id: null,
    result: "blocked",
    reason: "consent_revoked_by_creator",
    clearance_token: null,
  });

  return json({
    status: "revoked",
    creator_id,
    consent_id,
    revoked_at: now,
    message: "Consent revoked immediately. All further usage requests will be blocked.",
  });
}

async function handleStatus(creatorId: string, env: Env): Promise<Response> {
  if (!creatorId) {
    return json({ error: "Missing creator_id parameter" }, 400);
  }

  // HVS check
  const hvsRaw = await env.CONSENT_KV.get(`hvs:${creatorId}`);

  // Voice estate
  const estate = await env.AGENT_MEMORY.prepare(
    "SELECT * FROM voice_estate WHERE creator_id = ? LIMIT 1"
  )
    .bind(creatorId)
    .first<VoiceEstate>();

  // Active consent records
  const consents = await env.AGENT_MEMORY.prepare(
    "SELECT consent_id, status, usage_types, exclusions, granted_at, revoked_at FROM consent_records WHERE creator_id = ? ORDER BY granted_at DESC LIMIT 50"
  )
    .bind(creatorId)
    .all();

  // Recent events
  const events = await env.AGENT_MEMORY.prepare(
    "SELECT event_type, usage_type, result, reason, created_at FROM consent_events WHERE creator_id = ? ORDER BY created_at DESC LIMIT 20"
  )
    .bind(creatorId)
    .all();

  return json({
    creator_id: creatorId,
    hvs_registered: hvsRaw !== null,
    voice_estate: estate
      ? {
          display_name: estate.display_name,
          estate_status: estate.estate_status,
          royalty_rule: estate.royalty_rule,
        }
      : null,
    consent_records: consents.results,
    recent_events: events.results,
    queried_at: nowISO(),
  });
}

function handleHealth(): Response {
  return json({
    status: "ok",
    service: "consent-gateway",
    version: VERSION,
    timestamp: nowISO(),
  });
}

// ---------------------------------------------------------------------------
// Event logging helper
// ---------------------------------------------------------------------------

interface EventLogParams {
  creator_id: string;
  consent_id: string | null;
  event_type: string;
  usage_type: string | null;
  asset_ref: string | null;
  requestor_id: string | null;
  result: string;
  reason: string;
  clearance_token: string | null;
}

async function logEvent(env: Env, params: EventLogParams): Promise<void> {
  const id = crypto.randomUUID();
  try {
    await env.AGENT_MEMORY.prepare(
      `INSERT INTO consent_events (id, creator_id, consent_id, event_type, usage_type, asset_ref, requestor_id, result, reason, clearance_token, created_at)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
    )
      .bind(
        id,
        params.creator_id,
        params.consent_id,
        params.event_type,
        params.usage_type,
        params.asset_ref,
        params.requestor_id,
        params.result,
        params.reason,
        params.clearance_token,
        nowISO()
      )
      .run();
  } catch (err) {
    // Non-fatal: we never let logging failures block the consent pipeline
    console.error("Failed to log consent event:", err);
  }
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

    let response: Response;

    try {
      if (method === "POST" && path === "/verify") {
        response = await handleVerify(request, env);
      } else if (method === "POST" && path === "/revoke") {
        response = await handleRevoke(request, env);
      } else if (method === "GET" && path.startsWith("/status/")) {
        const creatorId = path.replace("/status/", "");
        response = await handleStatus(decodeURIComponent(creatorId), env);
      } else if (method === "GET" && path === "/health") {
        response = handleHealth();
      } else {
        response = json({ error: "Not found", path }, 404);
      }
    } catch (err) {
      console.error("Consent gateway error:", err);
      response = json(
        {
          error: "Internal server error",
          message: err instanceof Error ? err.message : "Unknown error",
        },
        500
      );
    }

    return withCors(response, origin, allowedOrigins);
  },
};
