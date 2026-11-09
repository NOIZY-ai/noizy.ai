/**
 * Voice Worker - Full Stack
 * Handles /generate, /personas, /audit
 */

import { PERSONAS } from "./personas";
import { DSP_PRESETS } from "./dsp-presets";

export interface Env {
    ANTHROPIC_API_KEY: string;
    TTS_API_KEY: string;
    TTS_ENDPOINT?: string;
    VOICE_BUCKET: R2Bucket;
    VOICE_AUDIT: KVNamespace;
}

interface GenerateRequest {
    text: string;
    personaId?: string;
    dspId?: string;
    rewrite?: boolean; // If true, uses Anthropic to rewrite text based on Persona
}

export default {
    async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
        const url = new URL(request.url);

        // === ROUTER ===

        // 1. GET /personas
        if (request.method === "GET" && url.pathname === "/personas") {
            return Response.json({ personas: PERSONAS, dsp: DSP_PRESETS });
        }

        // 2. GET /audit
        if (request.method === "GET" && url.pathname === "/audit") {
            // Basic audit log viewer using KV list
            const list = await env.VOICE_AUDIT.list({ limit: 20 });
            const logs = [];
            for (const key of list.keys) {
                const val = await env.VOICE_AUDIT.get(key.name);
                if (val) logs.push(JSON.parse(val));
            }
            return Response.json({ logs });
        }

        // 3. POST /generate
        if (request.method === "POST" && url.pathname === "/generate") {
            try {
                const body = await request.json() as GenerateRequest;

                // Validation
                if (!body.text) return new Response("Missing 'text'", { status: 400 });

                // Resolve Config
                const persona = PERSONAS.find(p => p.id === body.personaId) || PERSONAS[0]; // Default to first
                const dsp = DSP_PRESETS.find(d => d.id === body.dspId) || DSP_PRESETS[0];

                let textToSpeak = body.text;

                // A. Rewrite Step (Anthropic)
                if (body.rewrite) {
                    // Implement Anthropic Call for Rewrite
                    const claudeResp = await fetch("https://api.anthropic.com/v1/messages", {
                        method: "POST",
                        headers: {
                            "x-api-key": env.ANTHROPIC_API_KEY,
                            "anthropic-version": "2023-06-01",
                            "content-type": "application/json"
                        },
                        body: JSON.stringify({
                            model: "claude-3-haiku-20240307", // Fast model for rewrite
                            max_tokens: 256,
                            system: persona.systemPrompt + " Rewrite the following text to match your persona. Return ONLY the rewriten text, no quotes.",
                            messages: [{ role: "user", content: body.text }]
                        })
                    });

                    if (claudeResp.ok) {
                        const claudeJson: any = await claudeResp.json();
                        if (claudeJson.content && claudeJson.content[0]?.text) {
                            textToSpeak = claudeJson.content[0].text;
                        }
                    }
                }

                // B. TTS Step (ElevenLabs)
                // Hardcoded endpoint for now, or dynamic based on Voice ID
                const voiceId = persona.voiceId;
                const ttsUrl = `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`;

                const ttsResp = await fetch(ttsUrl, {
                    method: "POST",
                    headers: {
                        "xi-api-key": env.TTS_API_KEY,
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        text: textToSpeak,
                        model_id: "eleven_monolingual_v1",
                        voice_settings: dsp.settings
                    })
                });

                if (!ttsResp.ok) {
                    return new Response(`TTS Error: ${await ttsResp.text()}`, { status: ttsResp.status });
                }

                const audioBuffer = await ttsResp.arrayBuffer();

                // C. Storage Step (R2)
                const id = crypto.randomUUID();
                const objectKey = `audio/${id}.mp3`;
                await env.VOICE_BUCKET.put(objectKey, audioBuffer, {
                    httpMetadata: { contentType: "audio/mpeg" }
                });

                // D. Audit Step (KV)
                const auditEntry = {
                    id,
                    timestamp: new Date().toISOString(),
                    persona: persona.name,
                    dsp: dsp.name,
                    originalText: body.text,
                    spokenText: textToSpeak,
                    rewritten: !!body.rewrite,
                    key: objectKey
                };
                // Use expiration to auto-cleanup logs after 7 days (604800s)
                await env.VOICE_AUDIT.put(id, JSON.stringify(auditEntry), { expirationTtl: 604800 });

                // E. Return
                return Response.json({
                    status: "ok",
                    data: {
                        id,
                        url: `/${objectKey}`, // Client can fetch from R2 via worker if mapped, or just use ID
                        text: textToSpeak,
                        persona: persona.name
                    }
                });

            } catch (e) {
                return new Response(`Worker Error: ${e}`, { status: 500 });
            }
        }

        // Default
        return new Response("Voice Worker Online. Endpoints: /generate, /personas, /audit", { status: 200 });
    },
};
