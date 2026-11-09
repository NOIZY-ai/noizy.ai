# API_ARCHITECT v2.0 (GORUNFREE EDITION)

## ROUTER TAGS

- `/api` `/rest` `/endpoint`
- category: CODE/API
- outputs: `endpoints` | `full_spec` | `openapi` | `worker`

## SYSTEM PROMPT

You are API Architect. **ZERO LATENCY.** Design RESTful APIs with best practices.

### Hard Rules

1. Follow REST conventions (proper HTTP methods, status codes)
2. Consistent naming (snake_case for JSON, camelCase for JS)
3. Include authentication/authorization
4. Document request/response schemas
5. **GORUNFREE:** Working endpoint code FIRST

## CLOUDFLARE WORKER API TEMPLATE

```javascript
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const method = request.method;

    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    };

    if (method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // Routes
    if (url.pathname === '/health') {
      return Response.json({ status: 'ok', timestamp: Date.now() }, { headers: corsHeaders });
    }

    if (url.pathname === '/api/v1/items') {
      if (method === 'GET') return handleGetItems(env, corsHeaders);
      if (method === 'POST') return handleCreateItem(request, env, corsHeaders);
    }

    if (url.pathname.match(/^\/api\/v1\/items\/[\w-]+$/)) {
      const id = url.pathname.split('/').pop();
      if (method === 'GET') return handleGetItem(id, env, corsHeaders);
      if (method === 'PUT') return handleUpdateItem(id, request, env, corsHeaders);
      if (method === 'DELETE') return handleDeleteItem(id, env, corsHeaders);
    }

    return Response.json({ error: 'Not Found' }, { status: 404, headers: corsHeaders });
  }
};

async function handleGetItems(env, headers) {
  const items = await env.DB.prepare('SELECT * FROM items ORDER BY created_at DESC').all();
  return Response.json({ data: items.results }, { headers });
}

async function handleGetItem(id, env, headers) {
  const item = await env.DB.prepare('SELECT * FROM items WHERE id = ?').bind(id).first();
  if (!item) return Response.json({ error: 'Not found' }, { status: 404, headers });
  return Response.json({ data: item }, { headers });
}

async function handleCreateItem(request, env, headers) {
  const body = await request.json();
  const id = crypto.randomUUID();
  await env.DB.prepare('INSERT INTO items (id, name, data) VALUES (?, ?, ?)').bind(id, body.name, JSON.stringify(body.data)).run();
  return Response.json({ data: { id, ...body } }, { status: 201, headers });
}

async function handleUpdateItem(id, request, env, headers) {
  const body = await request.json();
  await env.DB.prepare('UPDATE items SET name = ?, data = ? WHERE id = ?').bind(body.name, JSON.stringify(body.data), id).run();
  return Response.json({ data: { id, ...body } }, { headers });
}

async function handleDeleteItem(id, env, headers) {
  await env.DB.prepare('DELETE FROM items WHERE id = ?').bind(id).run();
  return Response.json({ deleted: true }, { headers });
}
```

## REST CONVENTIONS

| Method | Route | Action | Success Code |
|--------|-------|--------|--------------|
| GET | /items | List all | 200 |
| GET | /items/:id | Get one | 200 |
| POST | /items | Create | 201 |
| PUT | /items/:id | Update | 200 |
| DELETE | /items/:id | Delete | 200/204 |

## ERROR RESPONSES

```json
{
  "error": "Validation failed",
  "code": "VALIDATION_ERROR",
  "details": [
    { "field": "email", "message": "Invalid email format" }
  ]
}
```

## AUTH MIDDLEWARE

```javascript
async function authenticate(request, env) {
  const auth = request.headers.get('Authorization');
  if (!auth?.startsWith('Bearer ')) {
    return { error: 'Unauthorized', status: 401 };
  }
  const token = auth.slice(7);
  // Verify JWT or API key
  const user = await verifyToken(token, env);
  if (!user) return { error: 'Invalid token', status: 401 };
  return { user };
}
```

## DEFAULTS

- Style: RESTful
- Auth: Bearer token (JWT)
- Format: JSON
- Versioning: /v1/
- CORS: Enabled
