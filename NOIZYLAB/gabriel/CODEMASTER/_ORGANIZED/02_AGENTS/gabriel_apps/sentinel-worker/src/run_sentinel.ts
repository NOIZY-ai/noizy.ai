import { MemCellStore } from "../../packages/memcell/src/index.js";

type Signal = { name: string; impact: number; urgency: number; evidence: string };

export async function runSentinelOnce(opts: {
    memRoot: string;
    fetchIntel: () => Promise<string>;
    analyze: (raw: string) => Promise<{ tldr: string[]; signals: Signal[]; actions: string[] }>;
}) {
    const mem = new MemCellStore(opts.memRoot);

    const raw = await opts.fetchIntel();
    const result = await opts.analyze(raw);

    const id = `mc_${new Date().toISOString().replace(/[-:.TZ]/g, "").slice(0, 14)}_sentinel_brief`;
    mem.upsert({
        id,
        type: "artifact",
        title: "Daily Sentinel Brief",
        summary: result.tldr.join(" | "),
        data: { tldr: result.tldr, signals: result.signals, actions: result.actions, raw_sample: raw.slice(0, 2000) },
        provenance: { source: "sentinel-worker", captured_at: new Date().toISOString(), author: "GABRIEL" },
        confidence: 0.75,
        checks: [{ method: "cross_source", result: "pending", notes: "Add 2nd source for verification." }],
        links: [],
        tags: ["sentinel", "mc96", "gabriel"],
    });

    return result;
}
