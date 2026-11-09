import { PersonaPack } from './persona-generator';
import { DSPEngine } from './dsp-engine';
import { DSP_PRESETS } from './dsp-presets';
import { PERSONAS } from './personas'; // Legacy/Static list, eventually replace with D1
import personaPacks from '../examples/persona-packs.json'; // The new production packs

export interface PerformanceRequest {
    text: string;
    personaId: string;
    environmentId?: string; // e.g., 'cathedral'
}

export interface PerformanceResult {
    ssml: string;
    dspFilter: string;
    meta: any;
}

export class PerformanceEngineer {

    /**
     * Orchestrates the transformation from Intent -> Spec.
     */
    static designPerformance(req: PerformanceRequest): PerformanceResult {
        // 1. Find the Persona Pack
        // Check dynamic/json packs first
        const pack = (personaPacks as any[]).find(p => p.persona_id === req.personaId);

        // Fallback to legacy static types if needed, or default
        if (!pack) {
            throw new Error(`Persona ${req.personaId} not found.`);
        }

        // 2. Generate SSML
        // Inject text into the template
        // "SSML_template": "<speak><prosody ...>{{TEXT}}</prosody></speak>"
        let ssml = pack.SSML_template.replace('{{TEXT}}', req.text);

        // 3. Design DSP Chain
        // Use the DSP Engine to build the filter string based on Persona + Environment
        const recipe = DSPEngine.generateRecipe(req.personaId, req.environmentId || 'studio');

        return {
            ssml,
            dspFilter: recipe.ffmpeg_filter,
            meta: {
                persona: pack.display_name,
                archetype: pack.archetype_tags[0],
                environment: recipe.environment.name,
                lufs: recipe.environment.lufs_target
            }
        };
    }
}
