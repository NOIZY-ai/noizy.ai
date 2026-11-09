import { Anthropic } from '@anthropic-ai/sdk';

// --- TYPES ---

export interface VoiceAnalysis {
    timbre: string;
    range: string;
    natural_prosody: string;
    suggested_archetypes: string[];
}

export interface ArtistContext {
    name: string;
    voiceDescription: string;
    specialties: string[];
    targetUseCases: string[];
}

export interface PersonaPack {
    persona_id: string;
    display_name: string;
    archetype_tags: string[];
    short_bio: string;
    recommended_prosody: {
        rate: string;
        pitch: string;
        volume: string;
    };
    SSML_template: string;
    DSP_recipe: {
        eq: string;
        compression: string;
        reverb: string;
    };
    animation_cues: {
        default_pose: string;
        signature_gesture: string;
        expression_range: string[];
        movement_style: string;
    };
}

// --- CONSTANTS ---

export const ARCHETYPES = [
    "Thunder Titan", "Solar Sentinel", "Void Ranger", "Mythic Architect",
    "Velvet Shadow", "Silk Whisper", "Steel Phoenix", "Ember Heart",
    "Iron Sage", "Liquid Neon"
];

export const DSP_PRESETS = [
    "broadcast", "cinematic", "vintage", "clean_studio", "ethereal_hall", "telephone_lofi"
];

// --- GENERATOR LOGIC ---

export class PersonaGenerator {
    private anthropic: Anthropic;

    constructor(apiKey: string) {
        this.anthropic = new Anthropic({ apiKey });
    }

    async generatePersonaPack(context: ArtistContext): Promise<PersonaPack> {
        const prompt = `
      You are the NOIZYVOX Persona Architect.
      Create a "Persona Pack" for a voice artist based on their profile.

      ARTIST CONTEXT:
      Name: ${context.name}
      Voice: ${context.voiceDescription}
      Specialties: ${context.specialties.join(", ")}
      Targets: ${context.targetUseCases.join(", ")}

      AVAILABLE ARCHETYPES: ${ARCHETYPES.join(", ")}
      AVAILABLE DSP PRESETS: ${DSP_PRESETS.join(", ")}

      Your goal is to create a distinct, marketable persona that amplifies their natural strengths.
      Return ONLY a valid JSON object matching this structure:
      {
        "persona_id": "kebab-case-id",
        "display_name": "Name",
        "archetype_tags": ["Archetype", "tag1", "tag2"],
        "short_bio": "2 sentence description.",
        "recommended_prosody": { "rate": "x%", "pitch": "+/-xst", "volume": "desc" },
        "SSML_template": "<speak>...</speak>",
        "DSP_recipe": { "eq": "preset", "compression": "preset", "reverb": "preset" },
        "animation_cues": {
           "default_pose": "desc",
           "signature_gesture": "desc",
           "expression_range": ["exp1", "exp2"],
           "movement_style": "desc"
        }
      }
    `;

        const msg = await this.anthropic.messages.create({
            model: "claude-3-5-sonnet-20241022",
            max_tokens: 1024,
            system: "You are a JSON-only generator for Voice Persona Packs.",
            messages: [{ role: "user", content: prompt }]
        });

        try {
            // Safe parsing of the text content
            const contentBlock = msg.content[0];
            if (contentBlock.type === 'text') {
                return JSON.parse(contentBlock.text);
            } else {
                throw new Error("Unexpected content block type from Claude");
            }
        } catch (e) {
            console.error("Failed to parse persona pack:", e);
            throw new Error("Persona generation failed.");
        }
    }
}
