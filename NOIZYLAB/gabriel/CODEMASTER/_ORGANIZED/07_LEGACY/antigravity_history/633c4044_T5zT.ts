/**
 * GOVERNANCE
 * Handles Provenance, Policy, and Rate Limiting.
 */

export interface VoiceManifest {
    id: string;
    timestamp: string;
    requesterIp: string;
    policyVersion: string;
    content: {
        textHash: string;
        personaId: string;
        backend: string;
    };
    signature?: string; // Placeholder for crypto signature
}

export class GovernanceEngine {
    constructor(private kv: KVNamespace) { }

    async createManifest(req: Request, text: string, personaId: string, backend: string): Promise<VoiceManifest> {
        const encoder = new TextEncoder();
        const data = encoder.encode(text);
        const textHash = await crypto.subtle.digest("SHA-256", data).then(b =>
            Array.from(new Uint8Array(b)).map(b => b.toString(16).padStart(2, '0')).join('')
        );

        return {
            id: crypto.randomUUID(),
            timestamp: new Date().toISOString(),
            requesterIp: req.headers.get("CF-Connecting-IP") || "unknown",
            policyVersion: "1.0.0",
            content: {
                textHash,
                personaId,
                backend
            }
        };
    }

    async checkRateLimit(ip: string): Promise<boolean> {
        const key = `ratelimit:${ip}`;
        const count = await this.kv.get(key);
        if (!count) {
            await this.kv.put(key, "1", { expirationTtl: 60 });
            return true;
        }
        if (parseInt(count) > 20) return false; // 20 req/min
        await this.kv.put(key, (parseInt(count) + 1).toString(), { expirationTtl: 60 });
        return true;
    }
}
