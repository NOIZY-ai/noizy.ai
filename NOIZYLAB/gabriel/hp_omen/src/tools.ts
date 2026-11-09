/**
 * GABRIEL EMBEDDED FUNCTION CALLING
 * ═══════════════════════════════════════════════════════════════
 * Uses @cloudflare/ai-utils runWithTools for embedded execution
 * ═══════════════════════════════════════════════════════════════
 */

import { runWithTools, createToolsFromOpenAPISpec, autoTrimTools } from '@cloudflare/ai-utils';

// Tool with function implementations for embedded calling
export interface EmbeddedTool {
  name: string;
  description: string;
  parameters: {
    type: 'object';
    properties: Record<string, { type: string; description: string; enum?: string[] }>;
    required: string[];
  };
  function: (args: Record<string, unknown>) => Promise<unknown>;
}

// Create GABRIEL's embedded tools with actual function implementations
export function createGabrielTools(env: {
  MEMCELL: D1Database;
  GABRIEL_CACHE: KVNamespace;
  GABRIEL_STORAGE: R2Bucket;
  HP_OMEN_IP: string;
}): EmbeddedTool[] {
  return [
    {
      name: 'search_knowledge',
      description: 'Search GABRIEL knowledge base for information, patterns, or facts',
      parameters: {
        type: 'object',
        properties: {
          query: { type: 'string', description: 'Search query' },
          limit: { type: 'string', description: 'Max results (default: 5)' },
        },
        required: ['query'],
      },
      function: async (args) => {
        const query = args.query as string;
        const limit = parseInt(args.limit as string) || 5;
        const results = await env.MEMCELL.prepare(
          `SELECT content, category, tags FROM memories
           WHERE content LIKE ? OR tags LIKE ?
           ORDER BY access_count DESC
           LIMIT ?`
        ).bind(`%${query}%`, `%${query}%`, limit).all();
        return results.results;
      },
    },
    {
      name: 'remember',
      description: 'Store information in GABRIEL memory for future recall',
      parameters: {
        type: 'object',
        properties: {
          content: { type: 'string', description: 'What to remember' },
          category: { type: 'string', description: 'Category', enum: ['pattern', 'fact', 'preference', 'instruction'] },
          tags: { type: 'string', description: 'Comma-separated tags' },
        },
        required: ['content', 'category'],
      },
      function: async (args) => {
        await env.MEMCELL.prepare(
          `INSERT INTO memories (content, category, tags, created_at)
           VALUES (?, ?, ?, datetime('now'))`
        ).bind(args.content, args.category, args.tags || '').run();
        return { stored: true, content: args.content };
      },
    },
    {
      name: 'cache_get',
      description: 'Retrieve a cached value by key',
      parameters: {
        type: 'object',
        properties: {
          key: { type: 'string', description: 'Cache key' },
        },
        required: ['key'],
      },
      function: async (args) => {
        const value = await env.GABRIEL_CACHE.get(args.key as string);
        return { key: args.key, value, found: value !== null };
      },
    },
    {
      name: 'cache_set',
      description: 'Store a value in cache with optional TTL',
      parameters: {
        type: 'object',
        properties: {
          key: { type: 'string', description: 'Cache key' },
          value: { type: 'string', description: 'Value to cache' },
          ttl: { type: 'string', description: 'TTL in seconds (default: 3600)' },
        },
        required: ['key', 'value'],
      },
      function: async (args) => {
        const ttl = parseInt(args.ttl as string) || 3600;
        await env.GABRIEL_CACHE.put(args.key as string, args.value as string, { expirationTtl: ttl });
        return { cached: true, key: args.key, ttl };
      },
    },
    {
      name: 'fetch_web',
      description: 'Fetch content from a URL',
      parameters: {
        type: 'object',
        properties: {
          url: { type: 'string', description: 'URL to fetch' },
          extract: { type: 'string', description: 'What to extract', enum: ['text', 'json', 'headers'] },
        },
        required: ['url'],
      },
      function: async (args) => {
        try {
          const response = await fetch(args.url as string);
          const extract = args.extract || 'text';

          if (extract === 'json') {
            return await response.json();
          } else if (extract === 'headers') {
            const headers: Record<string, string> = {};
            response.headers.forEach((v, k) => headers[k] = v);
            return headers;
          }
          return await response.text();
        } catch (e) {
          return { error: String(e), url: args.url };
        }
      },
    },
    {
      name: 'hp_omen_status',
      description: 'Check HP-OMEN machine status',
      parameters: {
        type: 'object',
        properties: {
          endpoint: { type: 'string', description: 'Specific endpoint to check', enum: ['status', 'peers', 'discover'] },
        },
        required: [],
      },
      function: async (args) => {
        const endpoint = args.endpoint || 'status';
        try {
          const response = await fetch(`http://${env.HP_OMEN_IP}:5175/api/bridge/${endpoint}`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
          });
          return await response.json();
        } catch (e) {
          return { online: false, error: String(e), ip: env.HP_OMEN_IP };
        }
      },
    },
    {
      name: 'hp_omen_send',
      description: 'Send a message to HP-OMEN machine',
      parameters: {
        type: 'object',
        properties: {
          message: { type: 'string', description: 'Message to send' },
        },
        required: ['message'],
      },
      function: async (args) => {
        try {
          const response = await fetch(`http://${env.HP_OMEN_IP}:5175/api/bridge/receive`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ from: 'GABRIEL_WORKER', message: args.message }),
          });
          return await response.json();
        } catch (e) {
          return { sent: false, error: String(e) };
        }
      },
    },
    {
      name: 'storage_list',
      description: 'List files in GABRIEL R2 storage',
      parameters: {
        type: 'object',
        properties: {
          prefix: { type: 'string', description: 'Path prefix to filter' },
          limit: { type: 'string', description: 'Max results' },
        },
        required: [],
      },
      function: async (args) => {
        const options: R2ListOptions = {};
        if (args.prefix) options.prefix = args.prefix as string;
        if (args.limit) options.limit = parseInt(args.limit as string);

        const list = await env.GABRIEL_STORAGE.list(options);
        return {
          files: list.objects.map(o => ({
            key: o.key,
            size: o.size,
            uploaded: o.uploaded.toISOString(),
          })),
          truncated: list.truncated,
        };
      },
    },
    {
      name: 'storage_get',
      description: 'Get a file from GABRIEL R2 storage',
      parameters: {
        type: 'object',
        properties: {
          key: { type: 'string', description: 'File key/path' },
        },
        required: ['key'],
      },
      function: async (args) => {
        const object = await env.GABRIEL_STORAGE.get(args.key as string);
        if (!object) {
          return { found: false, key: args.key };
        }
        return {
          found: true,
          key: args.key,
          size: object.size,
          content: await object.text(),
        };
      },
    },
    {
      name: 'calculate',
      description: 'Perform mathematical calculations',
      parameters: {
        type: 'object',
        properties: {
          expression: { type: 'string', description: 'Math expression to evaluate (e.g., "2 + 2", "sqrt(16)")' },
        },
        required: ['expression'],
      },
      function: async (args) => {
        try {
          // Safe math evaluation
          const expr = (args.expression as string).replace(/[^0-9+\-*/().sqrt\s]/g, '');
          const result = Function(`'use strict'; return (${expr.replace(/sqrt/g, 'Math.sqrt')})`)();
          return { expression: args.expression, result };
        } catch (e) {
          return { expression: args.expression, error: 'Invalid expression' };
        }
      },
    },
  ];
}

// Execute embedded function calling with runWithTools
export async function executeWithTools(
  ai: Ai,
  prompt: string,
  tools: EmbeddedTool[],
  options?: {
    model?: string;
    streamFinalResponse?: boolean;
    maxRecursiveToolRuns?: number;
    verbose?: boolean;
    autoTrim?: boolean;
  }
): Promise<{ response: string; toolResults: unknown[] }> {
  const model = options?.model || '@hf/nousresearch/hermes-2-pro-mistral-7b';

  // Convert tools to runWithTools format
  const toolsForAI = tools.map(t => ({
    name: t.name,
    description: t.description,
    parameters: t.parameters,
    function: t.function,
  }));

  const response = await runWithTools(
    ai,
    model,
    {
      messages: [
        { role: 'system', content: 'You are GABRIEL, an advanced AI assistant with access to tools. Use them when needed to answer questions or complete tasks.' },
        { role: 'user', content: prompt },
      ],
      tools: toolsForAI,
    },
    {
      streamFinalResponse: options?.streamFinalResponse || false,
      maxRecursiveToolRuns: options?.maxRecursiveToolRuns || 5,
      verbose: options?.verbose || false,
      // Uncomment to enable auto-trimming of irrelevant tools
      // trimFunction: options?.autoTrim ? autoTrimTools : undefined,
    }
  );

  // Extract tool results from response
  const toolResults: unknown[] = [];

  if (typeof response === 'object' && 'response' in response) {
    return {
      response: (response as { response: string }).response,
      toolResults,
    };
  }

  // Handle streaming response
  if (response instanceof ReadableStream) {
    const reader = response.getReader();
    const decoder = new TextDecoder();
    let result = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      result += decoder.decode(value, { stream: true });
    }

    return { response: result, toolResults };
  }

  return { response: String(response), toolResults };
}

// Create tools from OpenAPI spec (for external API integration)
export async function createToolsFromAPI(specUrl: string, authConfig?: {
  apiKey?: string;
  bearerToken?: string;
}): Promise<EmbeddedTool[]> {
  const spec = await fetch(specUrl).then(r => r.text());

  const overrides: Array<{ matcher: RegExp; values: Record<string, string> }> = [];

  if (authConfig?.apiKey) {
    overrides.push({
      matcher: /.*/,
      values: { 'x-api-key': authConfig.apiKey },
    });
  }

  if (authConfig?.bearerToken) {
    overrides.push({
      matcher: /.*/,
      values: { 'Authorization': `Bearer ${authConfig.bearerToken}` },
    });
  }

  return await createToolsFromOpenAPISpec(spec, {
    overrides,
    options: { verbose: false },
  }) as unknown as EmbeddedTool[];
}
