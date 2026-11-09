import OpenAI from "openai";

export interface Env {
    OPENAI_API_KEY: string;
    VOICE_VAULT: R2Bucket;
}

export default {
    // 1. FAST RETRIEVAL (The API)
    async fetch(request: Request, env: Env): Promise<Response> {
        const url = new URL(request.url);

        // Manual Override: Generate specific hero voice on demand
        if (request.method === "POST") {
            const { text, archetype } = await request.json();
            return await generateHeroicAsset(text, archetype || "cosmic", env);
        }

        // Latest Briefing: Fetch the most recent mp3 from R2
        if (url.pathname === "/latest") {
            // Reverse-chronological listing relying on the timestamp key naming convention
            const list = await env.VOICE_VAULT.list({ limit: 1, prefix: "commander_" });
            if (!list.objects.length) return new Response("No briefing found", { status: 404 });

            const latestKey = list.objects[0].key;
            const object = await env.VOICE_VAULT.get(latestKey);

            return new Response(object.body, {
                headers: {
                    "Content-Type": "audio/mpeg",
                    "Cache-Control": "public, max-age=3600", // ⚡ EDGE CACHING (1 hour)
                    "Access-Control-Allow-Origin": "*"
                }
            });
        }

        return new Response("Sentinel Online.", { status: 200 });
    },

    // 2. AUTOMATIC INTELLIGENCE (The 7:00 AM Cron)
    async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext) {
        ctx.waitUntil(runStrategicBriefing(env));
    },
};

// --- CORE LOGIC ---

async function runStrategicBriefing(env: Env) {
    // A. The Input (Replace with real RSS/API)
    const intelSource = "https://feeds.feedburner.com/TechCrunch/headlines";
    const intelRaw = await fetch(intelSource).then(r => r.text());

    // B. The Brain (Smarter Prompt)
    const openai = new OpenAI({ apiKey: env.OPENAI_API_KEY });
    const scriptGen = await openai.chat.completions.create({
        model: "gpt-4o-mini", // Fast & Cheap
        messages: [
            { role: "system", content: "You are the Sentinel of YestTomora. Scan this data for HIGH-LEVEL STRATEGIC THREATS and OPPORTUNITIES. Ignore noise. Output a 30-second briefing script to be read by a commander. Tone: Stoic, Prescient, Final." },
            { role: "user", content: `Raw Data: ${intelRaw.substring(0, 3000)}` }
        ]
    });
    const script = scriptGen.choices[0].message.content;

    // C. The Voice & Storage
    // We use reverse-chronological naming so 'list' always finds the newest first
    // 9999999999999 is a safe constant to ensure reverse ordering when subtracting Date.now()
    const timestamp = 9999999999999 - Date.now();
    await generateHeroicAsset(script, `commander_${timestamp}`, env);
}

async function generateHeroicAsset(text: string, filenameKey: string, env: Env) {
    const openai = new OpenAI({ apiKey: env.OPENAI_API_KEY });

    const mp3 = await openai.audio.speech.create({
        model: "tts-1-hd",     // 🟢 BETTER: HD Quality
        voice: "onyx",         // The "Commander" Voice
        input: text,
        speed: 0.9,            // Gravitas
    });

    const audioBuffer = await mp3.arrayBuffer();

    // Store in Vault
    await env.VOICE_VAULT.put(`${filenameKey}.mp3`, audioBuffer, {
        customMetadata: { prompt: text.substring(0, 100) }
    });

    return new Response(audioBuffer, {
        headers: { "Content-Type": "audio/mpeg" }
    });
}
