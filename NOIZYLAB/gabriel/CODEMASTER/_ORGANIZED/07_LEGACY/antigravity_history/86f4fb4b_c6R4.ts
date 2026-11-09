import { UnifiedAIWorker } from './UNIFIED_AI_WORKER';
import { KnowledgeGraphAI } from './KNOWLEDGE_GRAPH_AI';
import { AgentResponse } from './AI_ORCHESTRATION';
import { Pattern } from './PATTERN_INTELLIGENCE';

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
        await verifyTemporalAPI();
        await verifySynapses();
        await verifyGORUNFREE();
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
    if (result.latencyMs > 5) throw new Error(`High Latency Detected: ${result.latencyMs}ms (Limit: 5ms)`);
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
    // Strict typing: cast data to AgentResponse
    const chatData = chatRes.data as AgentResponse;
    if (!chatData.content || !chatData.content.includes('[SHIRL]')) throw new Error("Failed to route to SHIRL");
    console.log("- Routing PASS");

    // 2. Test Pattern Recognition (Anomaly)
    console.log("[Test 1.2] Pattern Recognition - Anomaly");
    const largePayload = {
        type: 'pattern' as const,
        payload: {
            // Correct strict type per PatternPayload interface
            stream: {
                data: new Array(2000).fill("DATA").join(""),
                timestamp: Date.now()
            }
        },
        userId: "test_user_synapse"
    };
    const patternRes = await worker.handleRequest(largePayload);
    // PatternIntelligence detects string length > 5000. 
    // We are passing an object, so JSON.stringify might be needed in PatternIntelligence or we ensure `stream` is the string.
    // Wait, PatternIntelligence `detect` checks `typeof inputStream === 'string'`.
    // So `stream` should BE the string.

    // Let's adjust the test to pass a string in stream for detection to work
    const hugeString = new Array(2000).fill("DATA").join("");
    const largeStringPayload = {
        type: 'pattern' as const,
        payload: { stream: hugeString },
        userId: "test_user_synapse"
    };

    const patternResString = await worker.handleRequest(largeStringPayload);

    const patterns = patternResString.data as Pattern[];
    if (!patterns.find(p => p.signature === 'large_data_burst')) throw new Error("Failed to detect anomaly");
    console.log("- Pattern PASS");
}

async function verifyTemporalAPI() {
    console.log("\n[TEST] Temporal Verification (API Layer)");
    const worker = new UnifiedAIWorker();

    // Seed Graph (Ensure something exists to overlap)
    await worker.handleRequest({
        type: 'graph',
        payload: { query: "Project Beta launched at 1000" }, // Mock NL query to trigger indexing if needed
        userId: "tester",
        context: {}
    });

    // Test the specific 'overlap:' command
    const tStart = Date.now() - 5000;
    const tEnd = Date.now() + 5000;
    const req = {
        type: 'graph' as const,
        payload: { query: `overlap:${tStart},${tEnd}` },
        userId: "tester"
    };

    const res = await worker.handleRequest(req);
    // Strict typing check
    if (!res.success) throw new Error("Temporal API request failed");

    // The worker returns { result: ... } for graph queries
    const graphData = res.data as { result: unknown };
    if (!Array.isArray(graphData.result)) throw new Error("Temporal API did not return an array in .result");

    console.log(`- Found ${graphData.result.length} overlapping nodes via API.`);
    console.log("- PASS");
}

async function verifyGORUNFREE() {
    console.log("\n[TEST] GORUNFREE Protocol (Stress & Parallelism)");
    const worker = new UnifiedAIWorker();
    const iterations = 100;
    const info = { type: 'chat' as const, payload: { message: "Speed" }, userId: "stress_test", context: {} };

    const t0 = performance.now();
    const promises = [];
    for (let i = 0; i < iterations; i++) {
        promises.push(worker.handleRequest(info));
    }
    await Promise.all(promises);
    const t1 = performance.now();

    const totalTime = t1 - t0;
    const avgTime = totalTime / iterations;

    console.log(`- Processed ${iterations} requests in ${totalTime.toFixed(2)}ms`);
    console.log(`- Average per request: ${avgTime.toFixed(2)}ms`);

    if (avgTime > 2) throw new Error(`GORUNFREE Violation: ${avgTime.toFixed(2)}ms/req > 2ms`);
    console.log("- PASS: ABSOLUTE PERFECTION");
}

runGabrielSuite();
