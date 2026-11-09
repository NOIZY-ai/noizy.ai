/**
 * DSP PRESETS
 * Maps abstract sound profiles to ElevenLabs voice settings.
 */

export interface DSPPreset {
    id: string;
    name: string;
    settings: {
        stability: number;
        similarity_boost: number;
        style?: number;
        use_speaker_boost?: boolean;
    };
}

export const DSP_PRESETS: DSPPreset[] = [
    {
        id: "balanced",
        name: "Balanced (Default)",
        settings: {
            stability: 0.5,
            similarity_boost: 0.75,
            use_speaker_boost: true,
        },
    },
    {
        id: "stable",
        name: "Hyper-Stable (News)",
        settings: {
            stability: 0.8,
            similarity_boost: 0.8,
            style: 0.0,
            use_speaker_boost: true,
        },
    },
    {
        id: "expressive",
        name: "High Expression (Drama)",
        settings: {
            stability: 0.3,
            similarity_boost: 0.85,
            style: 0.5,
            use_speaker_boost: true,
        },
    },
    {
        id: "extreme",
        name: "Extreme Variation (Chaos)",
        settings: {
            stability: 0.1,
            similarity_boost: 0.5,
            use_speaker_boost: false,
        },
    },
];
