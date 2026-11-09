import { UnifiedAIWorker } from './UNIFIED_AI_WORKER';

async function verifySynapses() {
    console.log(">>> VERIFYING NEURAL ACTIVATION <<<");
    const worker = new UnifiedAIWorker();

    // 1. Test Smart Routing (Empathy test)
    console.log("[Test 1] Smart Routing - Empathy");
    const chatReq = {
        type: 'chat' as const,
        payload: "I feel really tired and worried about this code.",
        userId: "test_user",
        context: { lastAgent: 'GENERAL' }
    };
    const chatRes = await worker.handleRequest(chatReq);
    console.log("Result:", chatRes);
    if (!chatRes.data.content.includes('[SHIRL]')) throw new Error("Failed to route to SHIRL");

    // 2. Test Pattern Recognition (Anomaly)
    console.log("\n[Test 2] Pattern Recognition - Anomaly");
    const largePayload = {
        type: 'pattern' as const,
        payload: new Array(1000).fill("DATA").join(""),
        userId: "test_user"
    };
    const patternRes = await worker.handleRequest(largePayload);
    console.log("Result:", patternRes);
    if (!patternRes.data.find((p: any) => p.signature === 'large_data_burst')) throw new Error("Failed to detect anomaly");

    console.log("\n>>> ALL SYSTEMS NOMINAL <<<");
}

verifySynapses().catch(console.error);
