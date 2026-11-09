/**
 * UNIFIED_AI_WORKER.ts
 *
 * Description:
 * One API endpoint for all AI interaction. Handles Chat, Voice, Workflows,
 * Pattern Recognition, and Knowledge Graph updates.
 *
 * GOD MODE: ENABLED
 * STRICT MODE: ENABLED
 */

import { AiOrchestration, AgentPersona, ProcessingContext } from '../orchestration/AiOrchestration.js';
import { PatternIntelligence, Pattern } from '../intelligence/PatternIntelligence.js';
import { KnowledgeGraphAI, InteractionPayload } from '../graph/KnowledgeGraphAI.js';

export interface ChatPayload {
    message: string;
    agent?: AgentPersona;
}

export interface VoicePayload {
    audioBuffer: ArrayBuffer | Buffer | unknown;
    format?: 'wav' | 'mp3' | 'webm';
}

export interface WorkflowPayload {
    workflowId: string;
    parameters?: Record<string, unknown>;
}

export interface PatternPayload {
    stream: unknown;
    detectAnomalies?: boolean;
}

export interface GraphPayload {
    query: string;
    operation?: 'query' | 'update' | 'delete';
}

export interface AIRequest {
    type: 'chat' | 'voice' | 'workflow' | 'pattern' | 'graph';
    payload: ChatPayload | VoicePayload | WorkflowPayload | PatternPayload | GraphPayload;
    context?: Record<string, unknown>;
    userId: string;
    requestId?: string;
}

export interface AIResponse<T = unknown> {
    success: boolean;
    data: T;
    latencyMs: number;
    requestId?: string;
    patterns?: Pattern[];
}

export class UnifiedAIWorker {
    private orchestrator: AiOrchestration;
    private patternIntel: PatternIntelligence;
    private knowledgeGraph: KnowledgeGraphAI;
    private requestCount: number;

    constructor() {
        this.orchestrator = new AiOrchestration();
        this.patternIntel = new PatternIntelligence();
        this.knowledgeGraph = new KnowledgeGraphAI();
        this.requestCount = 0;
    }

    public async handleRequest(request: AIRequest): Promise<AIResponse> {
        const startTime = Date.now();
        const requestId = request.requestId || `req_${++this.requestCount}_${Date.now()}`;
        let data: unknown = null;
        let detectedPatterns: Pattern[] = [];

        try {
            // Parallel Execution: Pattern Analysis + Memory Retrieval
            const [patterns, memoryContext] = await Promise.all([
                this.patternIntel.analyzeContext(request.context),
                this.retrieveContext(request.userId)
            ]);

            detectedPatterns = patterns;

            // Route Request
            switch (request.type) {
                case 'chat': {
                    const chatPayload = request.payload as ChatPayload;
                    data = await this.orchestrator.routeChat(
                        chatPayload.message,
                        memoryContext as ProcessingContext
                    );
                    break;
                }

                case 'voice': {
                    const voicePayload = request.payload as VoicePayload;
                    data = await this.orchestrator.processVoice(voicePayload.audioBuffer);
                    break;
                }

                case 'workflow': {
                    const workflowPayload = request.payload as WorkflowPayload;
                    data = await this.orchestrator.executeWorkflow(workflowPayload.workflowId);
                    break;
                }

                case 'pattern': {
                    const patternPayload = request.payload as PatternPayload;
                    data = await this.patternIntel.detect(patternPayload.stream);
                    break;
                }

                case 'graph': {
                    const graphPayload = request.payload as GraphPayload;
                    data = await this.knowledgeGraph.queryOrUpdate(graphPayload.query);
                    break;
                }

                default:
                    throw new Error(`Unknown request type: ${request.type}`);
            }

            // Auto-Knowledge Extraction (Async, non-blocking)
            this.backgroundKnowledgeUpdate(request, data, startTime);

        } catch (error) {
            console.error('[UnifiedAIWorker] Error:', error);
            return {
                success: false,
                data: error instanceof Error ? error.message : 'Unknown error',
                latencyMs: Date.now() - startTime,
                requestId
            };
        }

        return {
            success: true,
            data,
            latencyMs: Date.now() - startTime,
            requestId,
            patterns: detectedPatterns.length > 0 ? detectedPatterns : undefined
        };
    }

    private async retrieveContext(userId: string): Promise<ProcessingContext> {
        // In production, this would query user's session/memory
        return {
            lastAgent: 'GENERAL',
            userId,
            sessionStart: Date.now()
        };
    }

    private backgroundKnowledgeUpdate(
        request: AIRequest,
        responseData: unknown,
        timestamp: number
    ): void {
        // Non-blocking background task
        setImmediate(async () => {
            try {
                const interaction: InteractionPayload = {
                    input: request,
                    output: responseData,
                    timestamp,
                    userId: request.userId
                };
                await this.knowledgeGraph.extractAndStore(interaction);
            } catch (e) {
                console.error("[UnifiedAIWorker] Background knowledge update failed:", e);
            }
        });
    }

    // Utility methods

    public getOrchestrator(): AiOrchestration {
        return this.orchestrator;
    }

    public getPatternIntelligence(): PatternIntelligence {
        return this.patternIntel;
    }

    public getKnowledgeGraph(): KnowledgeGraphAI {
        return this.knowledgeGraph;
    }

    public getStats(): {
        requestCount: number;
        graphStats: unknown;
        patternStats: unknown;
        agents: string[];
    } {
        return {
            requestCount: this.requestCount,
            graphStats: this.knowledgeGraph.queryOrUpdate('stats'),
            patternStats: this.patternIntel.getStats(),
            agents: this.orchestrator.listAgents()
        };
    }
}

// Factory function
export function createWorker(): UnifiedAIWorker {
    return new UnifiedAIWorker();
}
