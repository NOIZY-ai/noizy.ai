import { KnowledgeGraphAI } from './KNOWLEDGE_GRAPH_AI';

async function verifyOmniscience() {
    console.log(">>> VERIFYING OMNISCIENCE (PHASE 4) <<<");
    const kg = new KnowledgeGraphAI();

    // 1. Test Temporal Extraction
    console.log("[Test 1] Temporal Extraction");
    const t0 = Date.now();
    await kg.extractAndStore({ input: "Project Alpha Launch", output: "Scheduled for Q4" });
    await new Promise(r => setTimeout(r, 10)); // Force time diff
    const t1 = Date.now();
    
    // Simulate overlap
    // Node A: t0 to t0
    // Node B: t0 to t1 (overlapping range)
    
    const range = { start: t0 - 100, end: t1 + 100 };
    const overlaps = kg.findTemporalOverlaps(range);
    
    console.log(`Found ${overlaps.length} temporal overlaps in range.`);
    if (overlaps.length === 0) throw new Error("Failed to find temporal overlaps");
    
    // 2. Verify Subject Type
    const subject = overlaps.find(n => n.type === 'subject');
    if (!subject) throw new Error("Failed to classify entity as SUBJECT");
    
    console.log("PASS: Temporal Knowledge Engine Active.");
    console.log("PASS: Subject Matter Classification Active.");
    console.log(">>> SYSTEM STATUS: GOD MODE <<<");
}

verifyOmniscience().catch(e => {
    console.error(e);
    process.exit(1);
});
