/**
 * Voice Worker - Voice Forge Orchestrator
 */

import { PERSONAS } from "./personas";
import { DSP_PRESETS } from "./dsp-presets";
import { GovernanceEngine } from "./governance";
import { TTSBackend, ElevenLabsBackend, TunnelBackend } from "./tts-backends";

export interface Env {
    ANTHROPIC_API_KEY: string;
    TTS_API_KEY: string;
    // Feature Flag: If set, use Tunnel. If empty, use ElevenLabs.
    LOCAL_TUNNEL_URL?: string;
    VOICE_BUCKET: R2Bucket;
    VOICE_AUDIT: KVNamespace;
}

interface GenerateRequest {
    text: string;
    personaId?: string;
    dspId?: string;
    rewrite?: boolean;
}

export default {
    async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
        const url = new URL(request.url);

        // 1. Governance Engine Init
        const gov = new GovernanceEngine(env.VOICE_AUDIT);
        const ip = request.headers.get("CF-Connecting-IP") || "local";

        // Check Rate Limit
        if (!(await gov.checkRateLimit(ip))) {
            return new Response("Rate Limit Exceeded", { status: 429 });
        }

        if (request.method === "POST" && url.pathname === "/generate") {
            try {
                const body = await request.json() as GenerateRequest;
                if (!body.text) return new Response("Missing 'text'", { status: 400 });

                // Config Loading
                const persona = PERSONAS.find(p => p.id === body.personaId) || PERSONAS[0];
                const dsp = DSP_PRESETS.find(d => d.id === body.dspId) || DSP_PRESETS[0];

                // A. Rewrite (Claude) - Keeping this Logic
                let textToSpeak = body.text;
                if (body.rewrite) {
                    const claudeResp = await fetch("https://api.anthropic.com/v1/messages", {
                        method: "POST",
                        headers: {
                            "x-api-key": env.ANTHROPIC_API_KEY,
                            "anthropic-version": "2023-06-01",
                            "content-type": "application/json"
                        },
                        body: JSON.stringify({
                            model: "claude-3-haiku-20240307",
                            max_tokens: 256,
                            system: persona.systemPrompt + " Rewrite instructions: Return ONLY the raw spoken text.",
                            messages: [{ role: "user", content: body.text }]
                        })
                    });
                    if (claudeResp.ok) {
                        const json: any = await claudeResp.json();
                        if (json.content?.[0]?.text) textToSpeak = json.content[0].text;
                    }
                }

                // B. Backend Selection
                let backend: TTSBackend;
                let backendName = "elevenlabs";

                if (env.LOCAL_TUNNEL_URL) {
                    backend = new TunnelBackend(env, env.LOCAL_TUNNEL_URL);
                    backendName = "local-tunnel";
                } else {
                    backend = new ElevenLabsBackend(env);
                }

                // C. Generation
                const audioResult = await backend.generate(textToSpeak, persona.voiceId, dsp.settings);

                // D. Manifest & Storage
                const manifest = await gov.createManifest(request, textToSpeak, persona.id, backendName);
                const objectKey = `audio/${manifest.id}.${audioResult.contentType === "audio/wav" ? "wav" : "mp3"}`;

                await env.VOICE_BUCKET.put(objectKey, audioResult.audio, {
                    httpMetadata: { contentType: audioResult.contentType },
                    customMetadata: { manifestId: manifest.id }
                });

                // E. Audit Log
                await env.VOICE_AUDIT.put(manifest.id, JSON.stringify({
                    ...manifest,
                    originalText: body.text,
                    spokenText: textToSpeak,
                    dsp: dsp.name
                }), { expirationTtl: 604800 });

                return Response.json({
                    status: "ok",
                    data: {
                        id: manifest.id,
                        url: `/${objectKey}`,
                        text: textToSpeak,
                        backend: backendName,
                        visemes: audioResult.visemes // Pass to frontend for animation
                    }
                });

            } catch (e: any) {
                return new Response(`Error: ${e.message}`, { status: 500 });
            }
        }

        // Pass-through for other endpoints (Propagate logic or re-implement if overwrite needed)
        // For simplicity, we just handle generate here.
        return new Response("Voice Forge Orchestrator Online", { status: 200 });
    },
};
