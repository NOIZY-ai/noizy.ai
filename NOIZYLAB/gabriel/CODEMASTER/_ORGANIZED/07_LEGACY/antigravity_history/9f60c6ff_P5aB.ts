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
        await verifySynapses();
    } catch (e) {
        console.error("!!! GABRIEL SUITE FAILED !!!", e);
        throw e;
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

async function verifySynapses() {
    console.log("\n[TEST] Synaptic Capability (Routing & Patterns)");
    const worker = new UnifiedAIWorker();

    // 1. Test Smart Routing (Empathy test)
    console.log("[Test 1.1] Smart Routing - Empathy");
    const chatReq = {
        type: 'chat' as const,
        payload: { message: "I feel really tired and worried about this code." },
        userId: "test_user_synapse",
        context: { lastAgent: 'GENERAL' as const }
    };
    const chatRes = await worker.handleRequest(chatReq);
    if (!chatRes.data.content.includes('[SHIRL]')) throw new Error("Failed to route to SHIRL");
    console.log("- Routing PASS");

    // 2. Test Pattern Recognition (Anomaly)
    console.log("[Test 1.2] Pattern Recognition - Anomaly");
    const largePayload = {
        type: 'pattern' as const,
        payload: { 
            data: new Array(2000).fill("DATA").join(""),
            timestamp: Date.now()
        },
        userId: "test_user_synapse"
    };
    const patternRes = await worker.handleRequest(largePayload);
    // We expect the pattern intelligence array to be returned in `data` (which is `any` in response but we should check)
    // The previous implementation returned { patterns: [...] } or the array itself.
    // Based on Unified Worker: `data: patterns`
    const patterns = patternRes.data as any[]; // We'll cast here for inspection as response.data is unknown/flexible
    if (!patterns.find(p => p.signature === 'large_data_burst')) throw new Error("Failed to detect anomaly");
    console.log("- Pattern PASS");
}

runGabrielSuite();
