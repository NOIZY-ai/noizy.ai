import { UnifiedAIWorker, AIRequest, AIResponse } from './UNIFIED_AI_WORKER';

/**
 * HEAVEN_WORKER.ts
 *
 * Description:
 * Main orchestrator. The "God Mode" entry point.
 * Commands, MemCells, Agent dispatch.
 * STRICT MODE: Enabled.
 */

export interface Env {
    MEMCELL: D1Database;
    AI_DISPATCH: Queue;
}

export default {
    async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
        const url = new URL(request.url);

        if (!request.headers.get('Authorization')) {
            return new Response('Unauthorized - GORUNFREE Protocol Violation', { status: 401 });
        }

        let body: unknown = {};
        if (request.method === 'POST') {
            body = await request.json();
        }

        // Safe casting or validation should occur here
        const safeBody = body as any; // In production, use Zod for validation

        const aiJob: AIRequest = {
            type: determineType(url.pathname),
            payload: safeBody,
            context: { timestamp: Date.now(), source: 'HEAVEN_WORKER' },
            userId: 'm2ultra' // default superuser
        };

        const unifiedWorker = new UnifiedAIWorker();
        const result = await unifiedWorker.handleRequest(aiJob);

        ctx.waitUntil(logToMemCell(env.MEMCELL, aiJob, result));

        return new Response(JSON.stringify(result), {
            headers: { 'Content-Type': 'application/json' }
        });
    }
};

function determineType(path: string): AIRequest['type'] {
    if (path.includes('chat')) return 'chat';
    if (path.includes('voice')) return 'voice';
    if (path.includes('pattern')) return 'pattern';
    if (path.includes('graph')) return 'graph';
    return 'workflow';
}

async function logToMemCell(db: D1Database, input: AIRequest, output: AIResponse) {
    try {
        const stmt = db.prepare('INSERT INTO logs (timestamp, input, output) VALUES (?, ?, ?)');
        const timestamp = Date.now();
        const inputStr = JSON.stringify(input);
        const outputStr = JSON.stringify(output);
        
        await stmt.bind(timestamp, inputStr, outputStr).run();
        
        if (output.latencyMs > 1000) {
             const pStmt = db.prepare('INSERT INTO patterns (id, signature, confidence, frequency, last_detected) VALUES (?, ?, ?, ?, ?) ON CONFLICT(id) DO UPDATE SET frequency = frequency + 1, last_detected = ?');
             await pStmt.bind('p_high_latency', 'high_latency', 1.0, 1, timestamp, timestamp).run();
        }

    } catch (e) {
        console.error('MemCell Write Failure:', e);
    }
}
