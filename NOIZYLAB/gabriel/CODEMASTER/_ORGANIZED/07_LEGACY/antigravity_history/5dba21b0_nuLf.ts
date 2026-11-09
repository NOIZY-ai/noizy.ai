import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

export type MemCell = {
    id: string;
    type: "fact" | "preference" | "source" | "plan" | "decision" | "artifact";
    title: string;
    summary: string;
    data: Record<string, unknown>;
    provenance: { source: string; captured_at: string; author: "GABRIEL" | "Rob" };
    confidence: number;
    checks: { method: string; result: "pass" | "fail" | "pending"; notes: string }[];
    links: string[];
    tags: string[];
    integrity: { checksum: string };
};

export class MemCellStore {
    constructor(private rootDir: string) {
        fs.mkdirSync(rootDir, { recursive: true });
    }

    private checksum(payload: unknown) {
        const json = JSON.stringify(payload);
        return "sha256:" + crypto.createHash("sha256").update(json).digest("hex");
    }

    upsert(cell: Omit<MemCell, "integrity">): MemCell {
        const full: MemCell = { ...cell, integrity: { checksum: this.checksum(cell) } };
        const file = path.join(this.rootDir, `${full.id}.json`);
        fs.writeFileSync(file, JSON.stringify(full, null, 2), "utf-8");
        return full;
    }

    list(): MemCell[] {
        return fs
            .readdirSync(this.rootDir)
            .filter((f) => f.endsWith(".json"))
            .map((f) => JSON.parse(fs.readFileSync(path.join(this.rootDir, f), "utf-8")));
    }

    get(id: string): MemCell | null {
        const file = path.join(this.rootDir, `${id}.json`);
        return fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, "utf-8")) : null;
    }
}
