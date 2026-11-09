/**
 * AI COMPLETE BRAIN - Main Entry Point
 *
 * GABRIEL System - Unified AI Integration
 * GOD MODE: ENABLED
 * STRICT MODE: ENABLED
 */

// Core exports
export { UnifiedAIWorker } from './workers/UnifiedAIWorker.js';
export type { AIRequest, AIResponse, ChatPayload, VoicePayload, WorkflowPayload, PatternPayload, GraphPayload } from './workers/UnifiedAIWorker.js';

export { AiOrchestration } from './orchestration/AiOrchestration.js';
export type { AgentPersona, AgentResponse, ProcessingContext } from './orchestration/AiOrchestration.js';

export { PatternIntelligence } from './intelligence/PatternIntelligence.js';
export type { Pattern } from './intelligence/PatternIntelligence.js';

export { KnowledgeGraphAI } from './graph/KnowledgeGraphAI.js';
export type { GraphNode, GraphEdge, TemporalRange, InteractionPayload } from './graph/KnowledgeGraphAI.js';

// Version info
export const VERSION = '1.0.0';
export const GOD_MODE = true;
export const STRICT_MODE = true;

// Quick start function
export async function createBrain(): Promise<UnifiedAIWorker> {
    const { UnifiedAIWorker } = await import('./workers/UnifiedAIWorker.js');
    return new UnifiedAIWorker();
}

// CLI entry point
if (import.meta.url === `file://${process.argv[1]}`) {
    console.log(`
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║              AI COMPLETE BRAIN - GABRIEL SYSTEM                  ║
║                                                                  ║
║         GOD MODE: ENABLED    STRICT MODE: ENABLED                ║
║                                                                  ║
║                     Version ${VERSION}                               ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
`);

    const brain = await createBrain();
    console.log('Brain initialized and ready.');
}
