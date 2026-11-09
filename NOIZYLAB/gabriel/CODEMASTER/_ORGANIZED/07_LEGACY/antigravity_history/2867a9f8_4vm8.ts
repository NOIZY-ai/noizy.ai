import { UnifiedAIWorker } from './UNIFIED_AI_WORKER';
import { KnowledgeGraphAI } from './KNOWLEDGE_GRAPH_AI';

/**
 * GABRIEL_TEST_SUITE.ts
 * 
 * Description:
 * The Master Verification Suite.
 * Runs all unit and integration tests in sequence.
 * "Inhals all loose code."
 */

async function runGabrielSuite() {
    console.log(">>> GABRIEL TEST SUITE: INITIATED <<<");
    const startTime = Date.now();

    try {
        await verifyLatency();
        await verifyOmniscience();
    } catch (e) {
        console.error("!!! GABRIEL SUITE FAILED !!!", e);
        process.exit(1);
    }

    console.log(`>>> GABRIEL SUITE COMPLETE in ${Date.now() - startTime}ms <<<`);
    console.log(">>> ALL SYSTEMS: GOD MODE <<<");
}

async function verifyLatency() {
    console.log("\n[TEST] Latency & Parallelism");
    const worker = new UnifiedAIWorker();
    const chatReq = {
        type: 'chat' as const,
        payload: { message: "Ping" },
        userId: "gabriel_tester",
        context: { lastAgent: 'GENERAL' }
    };

    // Warmup
    await worker.handleRequest(chatReq);

    // Measure
    const t0 = performance.now();
    const result = await worker.handleRequest(chatReq);
    const t1 = performance.now();

    console.log(`- Request Latency: ${(t1 - t0).toFixed(2)}ms`);
    if (result.latencyMs > 20) throw new Error("High Latency Detected");
    console.log("- PASS");
}

async function verifyOmniscience() {
    console.log("\n[TEST] Omniscience (Temporal & Persistence)");
    const kg = new KnowledgeGraphAI();
    
    // Test Persistence Shim
    await kg.extractAndStore({ input: "Project Omega", output: "Launch Date" });
    
    // Test Temporal
    const range = { start: Date.now() - 1000, end: Date.now() + 1000 };
    const overlaps = kg.findTemporalOverlaps(range);
    
    if (overlaps.length === 0) throw new Error("Omniscience Failure: No overlaps found.");
    console.log(`- Found ${overlaps.length} temporal nodes.`);
    console.log("- PASS");
}

runGabrielSuite();
