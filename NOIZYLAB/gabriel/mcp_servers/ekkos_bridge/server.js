#!/usr/bin/env node
/**
 * ekkOS MCP Bridge Server
 * Connects Claude to the ekkOS memory substrate (189 tables!)
 *
 * API: https://mcp.ekkos.dev
 */

const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');

const EKKOS_API = process.env.EKKOS_API_URL || 'https://mcp.ekkos.dev';
const USER_ID = process.env.EKKOS_USER_ID || 'system';
const AUTH_TOKEN = process.env.EKKOS_AUTH_TOKEN || '';

const server = new Server({
  name: 'ekkos-bridge',
  version: '1.0.0'
}, {
  capabilities: {
    tools: {},
    resources: {}
  }
});

// =============================================================================
// TOOLS
// =============================================================================

server.setRequestHandler('tools/list', async () => ({
  tools: [
    {
      name: 'search_memory',
      description: 'Search all 11 layers of ekkOS memory (patterns, directives, episodic, semantic, etc.)',
      inputSchema: {
        type: 'object',
        properties: {
          query: { type: 'string', description: 'Search query' },
          layers: {
            type: 'array',
            items: { type: 'string' },
            description: 'Layers to search: working, episodic, semantic, patterns, procedural, collective, codebase, directives'
          },
          limit: { type: 'number', default: 10 }
        },
        required: ['query']
      }
    },
    {
      name: 'forge_pattern',
      description: 'Create a new pattern from a solution you discovered',
      inputSchema: {
        type: 'object',
        properties: {
          title: { type: 'string', description: 'Pattern title' },
          problem: { type: 'string', description: 'Problem this pattern solves' },
          solution: { type: 'string', description: 'The solution/approach' },
          tags: { type: 'array', items: { type: 'string' } },
          confidence: { type: 'number', default: 0.85 }
        },
        required: ['title', 'problem', 'solution']
      }
    },
    {
      name: 'forge_directive',
      description: 'Create a user preference directive (MUST/NEVER/PREFER/AVOID)',
      inputSchema: {
        type: 'object',
        properties: {
          type: { type: 'string', enum: ['MUST', 'NEVER', 'PREFER', 'AVOID'] },
          rule: { type: 'string', description: 'The directive rule' },
          context: { type: 'string', description: 'When this applies' }
        },
        required: ['type', 'rule']
      }
    },
    {
      name: 'record_outcome',
      description: 'Record whether a pattern worked or failed',
      inputSchema: {
        type: 'object',
        properties: {
          pattern_id: { type: 'string' },
          success: { type: 'boolean' },
          notes: { type: 'string' }
        },
        required: ['pattern_id', 'success']
      }
    },
    {
      name: 'capture_event',
      description: 'Capture a memory event to the substrate',
      inputSchema: {
        type: 'object',
        properties: {
          event_type: { type: 'string' },
          content: { type: 'string' },
          metadata: { type: 'object' }
        },
        required: ['event_type', 'content']
      }
    },
    {
      name: 'get_memory_stats',
      description: 'Get statistics for all 11 memory layers',
      inputSchema: {
        type: 'object',
        properties: {}
      }
    },
    {
      name: 'recall_conversation',
      description: 'Recall past conversations by time or topic',
      inputSchema: {
        type: 'object',
        properties: {
          query: { type: 'string' },
          time_range: { type: 'string', description: 'e.g., "last_hour", "today", "this_week"' }
        }
      }
    }
  ]
}));

server.setRequestHandler('tools/call', async (request) => {
  const { name, arguments: args } = request.params;

  try {
    const result = await callEkkosAPI(name, args);
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  } catch (error) {
    return { content: [{ type: 'text', text: `Error: ${error.message}` }] };
  }
});

// =============================================================================
// RESOURCES
// =============================================================================

server.setRequestHandler('resources/list', async () => ({
  resources: [
    {
      uri: 'ekkos://patterns',
      name: 'Pattern Memory',
      description: 'All forged patterns',
      mimeType: 'application/json'
    },
    {
      uri: 'ekkos://directives',
      name: 'User Directives',
      description: 'MUST/NEVER/PREFER/AVOID rules',
      mimeType: 'application/json'
    },
    {
      uri: 'ekkos://stats',
      name: 'Memory Statistics',
      description: 'Stats across all 11 layers',
      mimeType: 'application/json'
    }
  ]
}));

server.setRequestHandler('resources/read', async (request) => {
  const { uri } = request.params;

  const result = await callEkkosAPI('get_resource', { uri });
  return { contents: [{ uri, text: JSON.stringify(result, null, 2), mimeType: 'application/json' }] };
});

// =============================================================================
// API HELPER
// =============================================================================

async function callEkkosAPI(action, params) {
  const endpoints = {
    search_memory: '/api/v1/context/retrieve',
    forge_pattern: '/api/v1/patterns',
    forge_directive: '/api/v1/directives',
    record_outcome: '/api/v1/patterns/outcome',
    capture_event: '/api/v1/memory/capture',
    get_memory_stats: '/api/v1/memory/stats',
    recall_conversation: '/api/v1/memory/recall',
    get_resource: '/api/v1/resources'
  };

  const endpoint = endpoints[action] || `/api/v1/${action}`;
  const method = ['search_memory', 'get_memory_stats', 'recall_conversation', 'get_resource'].includes(action) ? 'POST' : 'POST';

  const response = await fetch(`${EKKOS_API}${endpoint}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${AUTH_TOKEN}`,
      'X-User-ID': USER_ID
    },
    body: JSON.stringify({ ...params, user_id: USER_ID })
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

// =============================================================================
// MAIN
// =============================================================================

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('ekkOS MCP Bridge running...');
}

main().catch(console.error);
