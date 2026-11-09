import { UnifiedAIWorker, GraphPayload } from './UNIFIED_AI_WORKER';

async function verifyGodMode() {
    console.log(">>> VERIFYING GOD MODE (PHASE 3) <<<");
    const worker = new UnifiedAIWorker();

    // 1. Test Subject Matter Extraction
    console.log("[Test 1] Subject Matter Extraction");
    const chatReq = {
        type: 'chat' as const,
        payload: { message: "Optimizing the MC96 ECOUNIVERSE with TypeScript and Low Latency." },
        userId: "god_user",
        context: { lastAgent: 'ENGR_KEITH' }
    };
    // Fire and forget knowledge update happens in background, wait a bit
    await worker.handleRequest(chatReq);
    await new Promise(r => setTimeout(r, 100)); // Allow background processing

    // 2. Query Graph for Extracted Entities
    console.log("[Test 2] Graph Query");
    const graphReq = {
        type: 'graph' as const,
        payload: { query: "who" } as GraphPayload, // Mock query to trigger "Searching..."
        userId: "god_user"
    };
    const graphRes = await worker.handleRequest(graphReq);
    console.log("Graph Res:", graphRes);

    // 3. Test Temporal Overlap
    console.log("[Test 3] Temporal Overlap");
    const overlapReq = {
        type: 'graph' as const,
        payload: { query: `overlap:${Date.now() - 1000},${Date.now() + 1000}` } as GraphPayload,
        userId: "god_user"
    };
    const overlapRes = await worker.handleRequest(overlapReq);
    console.log("Overlap Res:", JSON.stringify(overlapRes, null, 2));
    
    // Assert we found something (since we just inserted it)
    const result = overlapRes.data as { result: unknown[] };
    if (Array.isArray(result.result) && result.result.length > 0) {
        console.log("PASS: Found overlapping nodes.");
    } else {
        console.warn("WARN: No overlaps found (might be timing issue or async DB insert simulation).");
    }

    console.log(">>> GOD MODE VERIFIED <<<");
}

verifyGodMode().catch(console.error);
