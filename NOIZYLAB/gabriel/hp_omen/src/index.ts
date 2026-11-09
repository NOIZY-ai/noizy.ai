/**
 * GABRIEL WORKERS AI CONTROLLER
 * ═══════════════════════════════════════════════════════════════
 * GABRIEL DIRECTS & CONTROLS ALL WORKERS AI INFERENCE
 *
 * Features:
 * - OpenAI-compatible API endpoint
 * - Native Batch API (queueRequest: true)
 * - Function Calling with tools
 * - AI SDK streaming support
 * - D1 MemCell persistence
 * - KV caching layer
 * - R2 storage integration
 * - Queue-based async processing
 * ═══════════════════════════════════════════════════════════════
 */

// Tool definition types for function calling
interface ToolParameter {
  type: string;
  description: string;
  enum?: string[];
}

interface ToolFunction {
  name: string;
  description: string;
  parameters: {
    type: 'object';
    properties: Record<string, ToolParameter>;
    required: string[];
  };
}

interface Tool {
  type: 'function';
  function: ToolFunction;
}

interface ToolCall {
  name: string;
  arguments: Record<string, unknown>;
}

// Import embedded tools
import { createGabrielTools, executeWithTools, EmbeddedTool } from './tools';

export interface Env {
  GABRIEL: Ai;
  MEMCELL: D1Database;
  GABRIEL_CACHE: KVNamespace;
  GABRIEL_STORAGE: R2Bucket;
  TASK_QUEUE: Queue;
  ENVIRONMENT: string;
  GABRIEL_VERSION: string;
  HP_OMEN_IP: string;
}

// Available Models - GABRIEL's Arsenal
const MODELS = {
  // Meta Llama
  LLAMA_70B: '@cf/meta/llama-3.3-70b-instruct-fp8-fast',
  LLAMA_8B: '@cf/meta/llama-3.1-8b-instruct',
  LLAMA_FAST: '@cf/meta/llama-3.2-3b-instruct',

  // DeepSeek
  DEEPSEEK_R1: '@cf/deepseek-ai/deepseek-r1-distill-qwen-32b',

  // Qwen
  QWEN_72B: '@cf/qwen/qwen2.5-72b-instruct',
  QWEN_CODER: '@cf/qwen/qwen2.5-coder-32b-instruct',

  // Embeddings
  BGE_LARGE: '@cf/baai/bge-large-en-v1.5',
  BGE_BASE: '@cf/baai/bge-base-en-v1.5',

  // Vision
  LLAVA: '@cf/llava-hf/llava-1.5-7b-hf',

  // Code
  DEEPSEEK_CODER: '@hf/thebloke/deepseek-coder-6.7b-instruct-awq',

  // Function Calling
  HERMES: '@hf/nousresearch/hermes-2-pro-mistral-7b',
} as const;

// GABRIEL's Built-in Tools for Function Calling
const GABRIEL_TOOLS: Tool[] = [
  {
    type: 'function',
    function: {
      name: 'search_memory',
      description: 'Search GABRIEL memory for relevant patterns, knowledge, or past interactions',
      parameters: {
        type: 'object',
        properties: {
          query: { type: 'string', description: 'The search query' },
          layer: { type: 'string', description: 'Memory layer to search', enum: ['patterns', 'episodic', 'semantic', 'all'] },
        },
        required: ['query'],
      },
    },
  },
  {
    type: 'function',
    function: {
      name: 'execute_code',
      description: 'Execute code in a sandboxed environment',
      parameters: {
        type: 'object',
        properties: {
          language: { type: 'string', description: 'Programming language', enum: ['javascript', 'python', 'typescript'] },
          code: { type: 'string', description: 'The code to execute' },
        },
        required: ['language', 'code'],
      },
    },
  },
  {
    type: 'function',
    function: {
      name: 'fetch_url',
      description: 'Fetch content from a URL',
      parameters: {
        type: 'object',
        properties: {
          url: { type: 'string', description: 'The URL to fetch' },
          method: { type: 'string', description: 'HTTP method', enum: ['GET', 'POST'] },
        },
        required: ['url'],
      },
    },
  },
  {
    type: 'function',
    function: {
      name: 'store_memory',
      description: 'Store information in GABRIEL memory for future recall',
      parameters: {
        type: 'object',
        properties: {
          content: { type: 'string', description: 'The content to remember' },
          category: { type: 'string', description: 'Memory category', enum: ['pattern', 'fact', 'preference', 'instruction'] },
          tags: { type: 'string', description: 'Comma-separated tags for retrieval' },
        },
        required: ['content', 'category'],
      },
    },
  },
  {
    type: 'function',
    function: {
      name: 'control_hp_omen',
      description: 'Send commands to HP-OMEN machine',
      parameters: {
        type: 'object',
        properties: {
          action: { type: 'string', description: 'Action to perform', enum: ['status', 'restart', 'deploy', 'sync'] },
          target: { type: 'string', description: 'Target service or path' },
        },
        required: ['action'],
      },
    },
  },
];

// GABRIEL Brain - Core AI Interface
class GabrielBrain {
  private ai: Ai;
  private cache: KVNamespace;
  private db: D1Database;

  constructor(env: Env) {
    this.ai = env.GABRIEL;
    this.cache = env.GABRIEL_CACHE;
    this.db = env.MEMCELL;
  }

  // Direct inference - GABRIEL speaks
  async think(prompt: string, model = MODELS.LLAMA_70B): Promise<string> {
    const cacheKey = `think:${this.hash(prompt + model)}`;

    // Check cache first
    const cached = await this.cache.get(cacheKey);
    if (cached) return cached;

    const response = await this.ai.run(model, {
      messages: [
        { role: 'system', content: 'You are GABRIEL, an advanced AI system. Be concise and precise.' },
        { role: 'user', content: prompt }
      ],
      max_tokens: 2048,
    }) as { response: string };

    // Cache for 1 hour
    await this.cache.put(cacheKey, response.response, { expirationTtl: 3600 });

    return response.response;
  }

  // Streaming response - GABRIEL flows
  async *stream(prompt: string, model = MODELS.LLAMA_70B): AsyncGenerator<string> {
    const response = await this.ai.run(model, {
      messages: [
        { role: 'system', content: 'You are GABRIEL. Respond with precision.' },
        { role: 'user', content: prompt }
      ],
      stream: true,
    });

    // @ts-ignore - Cloudflare AI streaming
    for await (const chunk of response) {
      if (chunk.response) {
        yield chunk.response;
      }
    }
  }

  // Embeddings - GABRIEL perceives
  async embed(text: string | string[], model = MODELS.BGE_LARGE): Promise<number[][]> {
    const texts = Array.isArray(text) ? text : [text];

    const response = await this.ai.run(model, {
      text: texts,
    }) as { data: Array<{ embedding: number[] }> };

    return response.data.map(d => d.embedding);
  }

  // Vision - GABRIEL sees
  async see(imageData: ArrayBuffer, prompt: string): Promise<string> {
    const response = await this.ai.run(MODELS.LLAVA, {
      image: [...new Uint8Array(imageData)],
      prompt: prompt,
      max_tokens: 1024,
    }) as { response: string };

    return response.response;
  }

  // Code - GABRIEL creates
  async code(prompt: string): Promise<string> {
    return this.think(prompt, MODELS.QWEN_CODER);
  }

  // Reason deeply - GABRIEL contemplates
  async reason(problem: string): Promise<string> {
    return this.think(problem, MODELS.DEEPSEEK_R1);
  }

  // Function Calling - GABRIEL acts
  async callWithTools(
    prompt: string,
    tools: Tool[],
    toolExecutors: Record<string, (args: Record<string, unknown>) => Promise<unknown>>
  ): Promise<{ response: string; toolCalls: Array<{ name: string; result: unknown }> }> {
    const toolCalls: Array<{ name: string; result: unknown }> = [];

    // First call - let model decide which tools to use
    const response = await this.ai.run(MODELS.HERMES, {
      messages: [
        { role: 'system', content: 'You are GABRIEL, an AI that can use tools to accomplish tasks. When you need to use a tool, respond with a JSON object containing "tool" and "arguments" keys.' },
        { role: 'user', content: prompt }
      ],
      tools: tools,
    }) as { response: string; tool_calls?: Array<{ name: string; arguments: string }> };

    // Execute any tool calls
    if (response.tool_calls && response.tool_calls.length > 0) {
      for (const call of response.tool_calls) {
        const executor = toolExecutors[call.name];
        if (executor) {
          const args = typeof call.arguments === 'string' ? JSON.parse(call.arguments) : call.arguments;
          const result = await executor(args);
          toolCalls.push({ name: call.name, result });
        }
      }

      // Second call - incorporate tool results
      const finalResponse = await this.ai.run(MODELS.HERMES, {
        messages: [
          { role: 'system', content: 'You are GABRIEL. Use the tool results to formulate your final response.' },
          { role: 'user', content: prompt },
          { role: 'assistant', content: JSON.stringify(response.tool_calls) },
          { role: 'user', content: `Tool results: ${JSON.stringify(toolCalls)}` }
        ],
      }) as { response: string };

      return { response: finalResponse.response, toolCalls };
    }

    return { response: response.response, toolCalls };
  }

  // Native Batch API - GABRIEL commands legions
  async batchInference(
    requests: Array<{ prompt: string; model?: string }>,
    queueRequest = true
  ): Promise<{ status: string; request_id?: string; responses?: unknown[] }> {
    const model = requests[0]?.model || MODELS.LLAMA_8B;

    const batchPayload = {
      requests: requests.map((r, idx) => ({
        messages: [
          { role: 'system', content: 'You are GABRIEL.' },
          { role: 'user', content: r.prompt }
        ],
        external_reference: `req_${idx}`,
      })),
    };

    const response = await this.ai.run(model, batchPayload, { queueRequest }) as {
      status?: string;
      request_id?: string;
      responses?: unknown[];
    };

    return {
      status: response.status || 'completed',
      request_id: response.request_id,
      responses: response.responses,
    };
  }

  // Poll Batch Status
  async pollBatch(requestId: string, model = MODELS.LLAMA_8B): Promise<unknown> {
    return await this.ai.run(model, { request_id: requestId });
  }

  private hash(str: string): string {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return hash.toString(36);
  }
}

// Batch Processor - GABRIEL commands many
class BatchProcessor {
  private queue: Queue;
  private db: D1Database;

  constructor(env: Env) {
    this.queue = env.TASK_QUEUE;
    this.db = env.MEMCELL;
  }

  async submit(tasks: Array<{ id: string; prompt: string; model?: string }>): Promise<string> {
    const batchId = crypto.randomUUID();

    // Store batch metadata
    await this.db.prepare(
      `INSERT INTO batches (id, task_count, status, created_at) VALUES (?, ?, 'queued', datetime('now'))`
    ).bind(batchId, tasks.length).run();

    // Queue all tasks
    for (const task of tasks) {
      await this.queue.send({
        batchId,
        taskId: task.id,
        prompt: task.prompt,
        model: task.model || MODELS.LLAMA_8B,
      });
    }

    return batchId;
  }

  async status(batchId: string): Promise<{ status: string; completed: number; total: number }> {
    const batch = await this.db.prepare(
      `SELECT * FROM batches WHERE id = ?`
    ).bind(batchId).first();

    if (!batch) throw new Error('Batch not found');

    const completed = await this.db.prepare(
      `SELECT COUNT(*) as count FROM batch_results WHERE batch_id = ?`
    ).bind(batchId).first() as { count: number };

    return {
      status: batch.status as string,
      completed: completed.count,
      total: batch.task_count as number,
    };
  }

  async results(batchId: string): Promise<Array<{ taskId: string; result: string }>> {
    const { results } = await this.db.prepare(
      `SELECT task_id, result FROM batch_results WHERE batch_id = ?`
    ).bind(batchId).all();

    return results.map(r => ({
      taskId: r.task_id as string,
      result: r.result as string,
    }));
  }
}

// OpenAI-Compatible Handler
async function handleOpenAICompatible(request: Request, env: Env): Promise<Response> {
  const url = new URL(request.url);
  const brain = new GabrielBrain(env);

  // Chat completions
  if (url.pathname === '/v1/chat/completions') {
    const body = await request.json() as {
      messages: Array<{ role: string; content: string }>;
      model?: string;
      stream?: boolean;
    };

    const model = body.model || MODELS.LLAMA_70B;
    const lastMessage = body.messages[body.messages.length - 1].content;

    if (body.stream) {
      const encoder = new TextEncoder();
      const stream = new ReadableStream({
        async start(controller) {
          for await (const chunk of brain.stream(lastMessage, model)) {
            const data = JSON.stringify({
              choices: [{ delta: { content: chunk } }]
            });
            controller.enqueue(encoder.encode(`data: ${data}\n\n`));
          }
          controller.enqueue(encoder.encode('data: [DONE]\n\n'));
          controller.close();
        }
      });

      return new Response(stream, {
        headers: {
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
        },
      });
    }

    const response = await brain.think(lastMessage, model);

    return Response.json({
      id: `chatcmpl-${crypto.randomUUID()}`,
      object: 'chat.completion',
      created: Math.floor(Date.now() / 1000),
      model: model,
      choices: [{
        index: 0,
        message: { role: 'assistant', content: response },
        finish_reason: 'stop',
      }],
    });
  }

  // Embeddings
  if (url.pathname === '/v1/embeddings') {
    const body = await request.json() as { input: string | string[]; model?: string };
    const embeddings = await brain.embed(body.input, body.model || MODELS.BGE_LARGE);

    const inputs = Array.isArray(body.input) ? body.input : [body.input];

    return Response.json({
      object: 'list',
      data: embeddings.map((embedding, index) => ({
        object: 'embedding',
        index,
        embedding,
      })),
      model: body.model || MODELS.BGE_LARGE,
      usage: { prompt_tokens: inputs.join('').length, total_tokens: inputs.join('').length },
    });
  }

  return Response.json({ error: 'Endpoint not found' }, { status: 404 });
}

// Main Request Handler
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    const brain = new GabrielBrain(env);
    const batch = new BatchProcessor(env);

    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    try {
      // OpenAI-compatible endpoints
      if (url.pathname.startsWith('/v1/')) {
        const response = await handleOpenAICompatible(request, env);
        // Add CORS headers to response
        const newHeaders = new Headers(response.headers);
        Object.entries(corsHeaders).forEach(([k, v]) => newHeaders.set(k, v));
        return new Response(response.body, { status: response.status, headers: newHeaders });
      }

      // GABRIEL Status
      if (url.pathname === '/api/status') {
        return Response.json({
          name: 'GABRIEL',
          version: env.GABRIEL_VERSION,
          environment: env.ENVIRONMENT,
          hp_omen_ip: env.HP_OMEN_IP,
          models: Object.keys(MODELS),
          capabilities: [
            'OpenAI-compatible API',
            'Function Calling (Traditional + Embedded)',
            'Native Batch API',
            'D1 MemCell Database',
            'KV Caching',
            'R2 Storage',
            'Queue Processing',
            'HP-OMEN Bridge Control',
          ],
          endpoints: {
            core: [
              'GET  /api/status',
              'POST /api/think',
              'POST /api/stream',
              'POST /api/embed',
              'POST /api/code',
              'POST /api/reason',
            ],
            openai: [
              'POST /v1/chat/completions',
              'POST /v1/embeddings',
            ],
            tools: [
              'GET  /api/tools/list',
              'POST /api/tools/call',
              'GET  /api/embedded/tools',
              'POST /api/embedded/call',
            ],
            batch: [
              'POST /api/batch/submit',
              'GET  /api/batch/status/:id',
              'GET  /api/batch/results/:id',
              'POST /api/native-batch/submit',
              'POST /api/native-batch/poll',
            ],
          },
          timestamp: new Date().toISOString(),
        }, { headers: corsHeaders });
      }

      // Direct Think
      if (url.pathname === '/api/think' && request.method === 'POST') {
        const { prompt, model } = await request.json() as { prompt: string; model?: string };
        const response = await brain.think(prompt, model);
        return Response.json({ response }, { headers: corsHeaders });
      }

      // Streaming Think
      if (url.pathname === '/api/stream' && request.method === 'POST') {
        const { prompt, model } = await request.json() as { prompt: string; model?: string };
        const encoder = new TextEncoder();

        const stream = new ReadableStream({
          async start(controller) {
            for await (const chunk of brain.stream(prompt, model)) {
              controller.enqueue(encoder.encode(chunk));
            }
            controller.close();
          }
        });

        return new Response(stream, {
          headers: {
            ...corsHeaders,
            'Content-Type': 'text/plain; charset=utf-8',
            'Transfer-Encoding': 'chunked',
          },
        });
      }

      // Embeddings
      if (url.pathname === '/api/embed' && request.method === 'POST') {
        const { text, model } = await request.json() as { text: string | string[]; model?: string };
        const embeddings = await brain.embed(text, model);
        return Response.json({ embeddings }, { headers: corsHeaders });
      }

      // Code Generation
      if (url.pathname === '/api/code' && request.method === 'POST') {
        const { prompt } = await request.json() as { prompt: string };
        const code = await brain.code(prompt);
        return Response.json({ code }, { headers: corsHeaders });
      }

      // Deep Reasoning
      if (url.pathname === '/api/reason' && request.method === 'POST') {
        const { problem } = await request.json() as { problem: string };
        const reasoning = await brain.reason(problem);
        return Response.json({ reasoning }, { headers: corsHeaders });
      }

      // Function Calling with Tools
      if (url.pathname === '/api/tools/call' && request.method === 'POST') {
        const { prompt, tools: customTools } = await request.json() as {
          prompt: string;
          tools?: Tool[];
        };

        // Use custom tools or GABRIEL's built-in tools
        const toolsToUse = customTools || GABRIEL_TOOLS;

        // Define tool executors
        const toolExecutors: Record<string, (args: Record<string, unknown>) => Promise<unknown>> = {
          search_memory: async (args) => {
            const query = args.query as string;
            const results = await env.MEMCELL.prepare(
              `SELECT * FROM memories WHERE content LIKE ? LIMIT 10`
            ).bind(`%${query}%`).all();
            return results;
          },
          execute_code: async (args) => {
            // Sandboxed code execution placeholder
            return { executed: true, language: args.language, output: 'Code execution simulated' };
          },
          fetch_url: async (args) => {
            const url = args.url as string;
            const method = (args.method as string) || 'GET';
            const response = await fetch(url, { method });
            return await response.text();
          },
          store_memory: async (args) => {
            await env.MEMCELL.prepare(
              `INSERT INTO memories (content, category, tags, created_at) VALUES (?, ?, ?, datetime('now'))`
            ).bind(args.content, args.category, args.tags || '').run();
            return { stored: true };
          },
          control_hp_omen: async (args) => {
            const action = args.action as string;
            const target = args.target as string;
            // Send command to HP-OMEN
            try {
              const response = await fetch(`http://${env.HP_OMEN_IP}:5175/api/bridge/${action}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ target }),
              });
              return await response.json();
            } catch (e) {
              return { error: 'HP-OMEN unreachable', action };
            }
          },
        };

        const result = await brain.callWithTools(prompt, toolsToUse, toolExecutors);
        return Response.json(result, { headers: corsHeaders });
      }

      // List Available Tools
      if (url.pathname === '/api/tools/list') {
        return Response.json({
          tools: GABRIEL_TOOLS.map(t => ({
            name: t.function.name,
            description: t.function.description,
            parameters: t.function.parameters,
          })),
        }, { headers: corsHeaders });
      }

      // Native Batch API - Submit
      if (url.pathname === '/api/native-batch/submit' && request.method === 'POST') {
        const { prompts, model, queue } = await request.json() as {
          prompts: string[];
          model?: string;
          queue?: boolean;
        };

        const requests = prompts.map(prompt => ({ prompt, model }));
        const result = await brain.batchInference(requests, queue !== false);
        return Response.json(result, { headers: corsHeaders });
      }

      // Native Batch API - Poll
      if (url.pathname === '/api/native-batch/poll' && request.method === 'POST') {
        const { request_id, model } = await request.json() as { request_id: string; model?: string };
        const result = await brain.pollBatch(request_id, model);
        return Response.json(result, { headers: corsHeaders });
      }

      // Embedded Function Calling with runWithTools
      if (url.pathname === '/api/embedded/call' && request.method === 'POST') {
        const { prompt, stream, maxRuns, verbose } = await request.json() as {
          prompt: string;
          stream?: boolean;
          maxRuns?: number;
          verbose?: boolean;
        };

        // Create tools with access to env bindings
        const embeddedTools = createGabrielTools({
          MEMCELL: env.MEMCELL,
          GABRIEL_CACHE: env.GABRIEL_CACHE,
          GABRIEL_STORAGE: env.GABRIEL_STORAGE,
          HP_OMEN_IP: env.HP_OMEN_IP,
        });

        const result = await executeWithTools(env.GABRIEL, prompt, embeddedTools, {
          streamFinalResponse: stream,
          maxRecursiveToolRuns: maxRuns || 5,
          verbose: verbose,
        });

        return Response.json(result, { headers: corsHeaders });
      }

      // List Embedded Tools
      if (url.pathname === '/api/embedded/tools') {
        const embeddedTools = createGabrielTools({
          MEMCELL: env.MEMCELL,
          GABRIEL_CACHE: env.GABRIEL_CACHE,
          GABRIEL_STORAGE: env.GABRIEL_STORAGE,
          HP_OMEN_IP: env.HP_OMEN_IP,
        });

        return Response.json({
          tools: embeddedTools.map(t => ({
            name: t.name,
            description: t.description,
            parameters: t.parameters,
          })),
          count: embeddedTools.length,
        }, { headers: corsHeaders });
      }

      // Batch Submit
      if (url.pathname === '/api/batch/submit' && request.method === 'POST') {
        const { tasks } = await request.json() as { tasks: Array<{ id: string; prompt: string; model?: string }> };
        const batchId = await batch.submit(tasks);
        return Response.json({ batchId, status: 'queued' }, { headers: corsHeaders });
      }

      // Batch Status
      const statusMatch = url.pathname.match(/^\/api\/batch\/status\/(.+)$/);
      if (statusMatch) {
        const status = await batch.status(statusMatch[1]);
        return Response.json(status, { headers: corsHeaders });
      }

      // Batch Results
      const resultsMatch = url.pathname.match(/^\/api\/batch\/results\/(.+)$/);
      if (resultsMatch) {
        const results = await batch.results(resultsMatch[1]);
        return Response.json({ results }, { headers: corsHeaders });
      }

      return Response.json({ error: 'Not found', path: url.pathname }, { status: 404, headers: corsHeaders });

    } catch (error) {
      console.error('GABRIEL Error:', error);
      return Response.json(
        { error: error instanceof Error ? error.message : 'Unknown error' },
        { status: 500, headers: corsHeaders }
      );
    }
  },

  // Queue Consumer - Process batch tasks
  async queue(batch: MessageBatch<{ batchId: string; taskId: string; prompt: string; model: string }>, env: Env): Promise<void> {
    const brain = new GabrielBrain(env);

    for (const message of batch.messages) {
      try {
        const { batchId, taskId, prompt, model } = message.body;
        const result = await brain.think(prompt, model);

        await env.MEMCELL.prepare(
          `INSERT INTO batch_results (batch_id, task_id, result, created_at) VALUES (?, ?, ?, datetime('now'))`
        ).bind(batchId, taskId, result).run();

        message.ack();
      } catch (error) {
        console.error('Queue processing error:', error);
        message.retry();
      }
    }
  },
};
