/**
 * GOVERNANCE - EXPANDED
 * Handles full provenance chain (Input Hash -> Audio Hash -> Manifest).
 */

export interface VoiceManifest {
    id: string;
    created_at: string;
    requester_ip: string;
    policy_version: string;
    provenance: {
        persona: string;
        claude_model: string;
        tts_engine: string;
        dsp_chain_id: string;
        input_text_hash: string;
        audio_hash: string; // SHA-256 of the generated audio blob
        signature?: string;
    };
    details: {
        rewrite_occurred: boolean;
        voice_id: string;
    };
}

export class GovernanceEngine {
    constructor(private kv: KVNamespace) { }

    async createManifest(
        req: Request,
        params: { text: string; persona: string; dsp: string; engine: string; rewrite: boolean; voiceId: string; model: string },
        audioBuffer: ArrayBuffer
    ): Promise<VoiceManifest> {

        // Hash Input Text
        const encoder = new TextEncoder();
        const textData = encoder.encode(params.text);
        const textHash = await this.sha256(textData);

        // Hash Audio Output
        const audioHash = await this.sha256(audioBuffer);

        return {
            id: crypto.randomUUID(),
            created_at: new Date().toISOString(),
            requester_ip: req.headers.get("CF-Connecting-IP") || "unknown",
            policy_version: "2.0.0",
            provenance: {
                persona: params.persona,
                claude_model: params.model,
                tts_engine: params.engine,
                dsp_chain_id: params.dsp,
                input_text_hash: textHash,
                audio_hash: audioHash,
            },
            details: {
                rewrite_occurred: params.rewrite,
                voice_id: params.voiceId
            }
        };
    }

    async checkRateLimit(ip: string): Promise<boolean> {
        const key = \`ratelimit:\${ip}\`;
    const count = await this.kv.get(key);
    if (!count) {
      await this.kv.put(key, "1", { expirationTtl: 60 });
      return true;
    }
    if (parseInt(count) > 50) return false; // Increased limit
    await this.kv.put(key, (parseInt(count) + 1).toString(), { expirationTtl: 60 });
    return true;
  }

  private async sha256(data: BufferSource): Promise<string> {
    const hashBuffer = await crypto.subtle.digest("SHA-256", data);
    return Array.from(new Uint8Array(hashBuffer))
      .map(b => b.toString(16).padStart(2, '0'))
      .join('');
  }
}
