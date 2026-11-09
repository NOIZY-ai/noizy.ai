/**
 * DSP ENGINE
 * Defines the rigorous audio specifications for the NOIZYVOX Forge.
 * Used to generate FFmpeg filter graphs and automation curves.
 */

// --- TYPES ---

export interface DSPEnvironment {
    id: string;
    name: string;
    reverb: {
        type: 'room' | 'hall' | 'cathedral' | 'plate' | 'stadium';
        wet: number; // 0.0 to 1.0
        decay: number; // Seconds
        damping?: number; // 0.0 to 1.0 (HF damping)
    };
    compression: {
        threshold: number; // dB
        ratio: number;
        attack: number; // ms
        release: number; // ms
        makeup: number; // dB
    };
    lufs_target: number;
}

export interface PersonaModifier {
    persona_id: string;
    pitch_shift: number; // Semitones
    formant_shift: number; // Semitones (approximate)
    eq: {
        low_shelf?: number; // dB
        mid_presence?: number; // dB
        high_shelf?: number; // dB
    };
}

export interface AutomationData {
    words: string[];
    timestamps: number[];
    f0_curve: number[]; // cents adjustment per word
    energy_curve: number[]; // dB adjustment per word
}

// --- PRESETS ---

export const ENVIRONMENTS: Record<string, DSPEnvironment> = {
    studio: {
        id: "studio",
        name: "Clean Studio",
        reverb: { type: "room", wet: 0.05, decay: 0.4, damping: 0.5 },
        compression: { threshold: -16, ratio: 3, attack: 5, release: 50, makeup: 2 },
        lufs_target: -16
    },
    cathedral: {
        id: "cathedral",
        name: "Gothic Cathedral",
        reverb: { type: "cathedral", wet: 0.35, decay: 3.5, damping: 0.2 },
        compression: { threshold: -20, ratio: 2, attack: 15, release: 100, makeup: 4 },
        lufs_target: -18
    },
    live: {
        id: "live",
        name: "Live Stadium",
        reverb: { type: "stadium", wet: 0.25, decay: 1.8, damping: 0.1 },
        compression: { threshold: -14, ratio: 5, attack: 2, release: 30, makeup: 6 },
        lufs_target: -14
    }
};

export const PERSONA_MODIFIERS: Record<string, PersonaModifier> = {
    "titan": {
        persona_id: "titan",
        pitch_shift: -2,
        formant_shift: -1,
        eq: { low_shelf: 4, mid_presence: 2, high_shelf: -2 }
    },
    "solar": {
        persona_id: "solar",
        pitch_shift: 0,
        formant_shift: 0,
        eq: { low_shelf: 1, mid_presence: 3 }
    },
    "void": {
        persona_id: "void",
        pitch_shift: -1,
        formant_shift: 0,
        eq: { low_shelf: -4, mid_presence: 5, high_shelf: 2 }
    },
    "architect": {
        persona_id: "architect",
        pitch_shift: -1.5,
        formant_shift: -0.5,
        eq: { low_shelf: 2, mid_presence: 0, high_shelf: 3 }
    },
    "shadow": {
        persona_id: "shadow",
        pitch_shift: 0,
        formant_shift: -0.5,
        eq: { low_shelf: 1, mid_presence: 0, high_shelf: -3 }
    },
    "whisper": {
        persona_id: "whisper",
        pitch_shift: 1,
        formant_shift: 0.5,
        eq: { low_shelf: -2, mid_presence: 2, high_shelf: 4 }
    }
};

// --- LOGIC ---

export class DSPEngine {
    static generateRecipe(personaId: string, envId: string = 'studio'): any {
        const mod = PERSONA_MODIFIERS[personaId] || PERSONA_MODIFIERS['solar']; // Default to solar
        const env = ENVIRONMENTS[envId] || ENVIRONMENTS['studio'];

        return {
            modifiers: mod,
            environment: env,
            ffmpeg_filter: this.buildFilterString(mod, env)
        };
    }

    private static buildFilterString(mod: PersonaModifier, env: DSPEnvironment): string {
        const filters: string[] = [];

        // 1. EQ
        let eqString = "";
        if (mod.eq.low_shelf) eqString += `firequalizer=gain=${mod.eq.low_shelf}:f=100:width_type=h,`;
        if (mod.eq.mid_presence) eqString += `firequalizer=gain=${mod.eq.mid_presence}:f=2500:width_type=q:w=1,`;
        if (mod.eq.high_shelf) eqString += `firequalizer=gain=${mod.eq.high_shelf}:f=10000:width_type=h,`;
        if (eqString) filters.push(eqString.replace(/,$/, ''));

        // 2. Pitch/Formant (Using rubberband if available, else standard pitch)
        // Note: Rubberband is computationally expensive, might need simple 'asetrate' for simple shifting
        if (mod.pitch_shift !== 0) {
            const scale = Math.pow(2, mod.pitch_shift / 12);
            // Simple pitch shift without time stretch correction (chipmunk effect) - usually not desired?
            // Actually creating a robust pitch shifting filter string purely in standard ffmpeg is tough.
            // We will output a placeholder instruction for the 'GOD' node which has rubberband.
            filters.push(`rubberband=pitch=${scale}`);
        }

        // 3. Compression
        filters.push(`acompressor=threshold=${env.compression.threshold}dB:ratio=${env.compression.ratio}:attack=${env.compression.attack}:release=${env.compression.release}:makeup=${env.compression.makeup}dB`);

        // 4. Reverb (Simulated with simple echo/delay or ir filters)
        if (env.reverb.wet > 0) {
            // Simple echo-based reverb simulation for FFmpeg string compatibility
            const decayMs = env.reverb.decay * 1000;
            filters.push(`aecho=0.8:0.9:${Math.floor(decayMs / 3)}:0.3`);
        }

        return filters.join(",");
    }
}
