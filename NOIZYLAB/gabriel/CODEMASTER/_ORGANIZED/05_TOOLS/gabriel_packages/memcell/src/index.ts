import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

export type MemCell = {
    id: string;
    type: "fact" | "concept" | "decision" | "artifact" | "source" | "conflict" | "preference" | "task";
    claim: string;
    summary: string;
    entities: string[];
    tags: string[];
    provenance: {
        source_ids: string[];
        captured_at: string;
        author: "GABRIEL" | "Rob";
    };
    evidence: {
        source_id: string;
        quote: string;
        locator?: string;
    }[];
    confidence: number;
    integrity: {
        input_hash: string;
        cell_hash: string;
    };
    links: {
        supports?: string[];
        contradicts?: string[];
        depends_on?: string[];
        related?: string[];
    };
    checks: {
        method: string;
        result: "pass" | "fail" | "pending";
        notes: string;
    }[];
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
        // Generate integrity hashes
        const inputJson = JSON.stringify(cell);
        const inputHash = "sha256:" + crypto.createHash("sha256").update(inputJson).digest("hex");

        // Construct full object without cell_hash first
        const wip: any = { ...cell, integrity: { input_hash: inputHash, cell_hash: "" } };

        // Calculate final cell hash (including input hash)
        const cellJson = JSON.stringify(wip);
        const cellHash = "sha256:" + crypto.createHash("sha256").update(cellJson).digest("hex");

        const full: MemCell = { ...cell, integrity: { input_hash: inputHash, cell_hash: cellHash } };
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
