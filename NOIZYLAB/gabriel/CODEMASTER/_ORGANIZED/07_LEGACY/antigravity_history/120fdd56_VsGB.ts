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

        // The original code had a general body parsing and then specific AI job creation.
        // The new code snippet provided in the instruction assumes that the POST request
        // directly contains an AIRequest and handles it within the POST block.
        // This means the subsequent AI job creation and worker dispatch logic
        // outside the POST block in the original code will be removed/replaced.

        if (request.method === 'POST') {
            try {
                const body = await request.json() as unknown;
                // Basic Type Guard Validation
                if (typeof body === 'object' && body !== null && 'type' in body) {
                    const aiRequest = body as AIRequest; // Assumed safe after basic check in this demo
                     
                    // AI Processing
                    const worker = new UnifiedAIWorker();
                    const result = await worker.handleRequest(aiRequest);

                    ctx.waitUntil(logToMemCell(env.MEMCELL, aiRequest, result)); // Log the request and result

                    return new Response(JSON.stringify(result, null, 2), {
                        headers: { 'Content-Type': 'application/json' }
                    });
                } else {
                     return new Response("Invalid Payload", { status: 400 });
                }
            } catch (e: unknown) { // Explicit unknown
                const error = e instanceof Error ? e.message : String(e);
                console.error(`[Worker Error] ${error}`);
                return new Response(`Error: ${error}`, { status: 500 });
            }
        }

        // If it's not a POST request or if the POST request didn't return a response,
        // we might need a default response or further handling.
        // For now, assuming POST is the primary interaction.
        return new Response("Method Not Allowed or No Matching Route", { status: 405 });
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
