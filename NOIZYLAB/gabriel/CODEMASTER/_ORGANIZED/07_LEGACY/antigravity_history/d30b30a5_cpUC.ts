/**
 * TTS BACKENDS
 * Strategy pattern for switching providers.
 */

import { Env } from "./index";

export interface AudioResult {
    audio: ArrayBuffer;
    contentType: string;
    backendMetadata: any;
}

export interface TTSBackend {
    generate(text: string, voiceId: string, settings?: any): Promise<AudioResult>;
}

export class ElevenLabsBackend implements TTSBackend {
    constructor(private env: Env) { }

    async generate(text: string, voiceId: string, settings?: any): Promise<AudioResult> {
        const url = \`https://api.elevenlabs.io/v1/text-to-speech/\${voiceId}\`;
    const resp = await fetch(url, {
      method: "POST",
      headers: {
        "xi-api-key": this.env.TTS_API_KEY,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        text,
        model_id: "eleven_monolingual_v1",
        voice_settings: settings
      })
    });

    if (!resp.ok) throw new Error(\`ElevenLabs Error: \${await resp.text()}\`);
    return {
      audio: await resp.arrayBuffer(),
      contentType: "audio/mpeg",
      backendMetadata: { provider: "elevenlabs", voiceId }
    };
  }
}

// Placeholder for Tunnel Backend - connects to local Docker stack via Cloudflare Access/Tunnel
export class TunnelBackend implements TTSBackend {
  constructor(private env: Env, private tunnelUrl: string) {}

  async generate(text: string, voiceId: string, settings?: any): Promise<AudioResult> {
    // Call local TTS service exposed via Tunnel
    // E.g., https://tts-api.mc96.fishmusicinc.com/generate
    const resp = await fetch(\`\${this.tunnelUrl}/generate\`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, voice: voiceId }) // Standardized internal API
    });

    if (!resp.ok) throw new Error(\`Tunnel Error: \${await resp.text()}\`);
    return {
      audio: await resp.arrayBuffer(),
      contentType: "audio/wav", // Local TTS likely generates WAV
      backendMetadata: { provider: "local-tunnel", endpoint: this.tunnelUrl }
    };
  }
}
