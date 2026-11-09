import { AiOrchestration, AgentPersona } from './AI_ORCHESTRATION';
import { PatternIntelligence, Pattern } from './PATTERN_INTELLIGENCE';
import { KnowledgeGraphAI } from './KNOWLEDGE_GRAPH_AI';

/**
 * UNIFIED_AI_WORKER.ts
 *
 * Description:
 * One API endpoint for all AI interaction. Handles Chat, Voice, Workflows,
 * Pattern Recognition, and Knowledge Graph updates.
 * STRICT MODE: Enabled.
 */

export interface AIRequest {
  type: 'chat' | 'voice' | 'workflow' | 'pattern' | 'graph';
  payload: ChatPayload | VoicePayload | WorkflowPayload | PatternPayload | GraphPayload;
  context?: Record<string, unknown>;
  userId: string;
}

export interface ChatPayload { message: string; agent?: string; }
export interface VoicePayload { audioBuffer: unknown; }
export interface WorkflowPayload { workflowId: string; }
export interface PatternPayload { stream: unknown; }
export interface GraphPayload { query: string; }

export interface AIResponse<T = unknown> {
  success: boolean;
  data: T;
  latencyMs: number;
}

export class UnifiedAIWorker {
  private orchestrator: AiOrchestration;
  private patternIntel: PatternIntelligence;
  private knowledgeGraph: KnowledgeGraphAI;

  constructor() {
    this.orchestrator = new AiOrchestration();
    this.patternIntel = new PatternIntelligence();
    this.knowledgeGraph = new KnowledgeGraphAI();
  }

  public async handleRequest(request: AIRequest): Promise<AIResponse> {
    const startTime = Date.now();
    let data: unknown = null;

    try {
      // Parallel Execution: Proactive Checks + Memory Retrieval
      const [_, memoryContext] = await Promise.all([
        this.patternIntel.analyzeContext(request.context),
        this.retrieveContext(request.userId)
      ]);

      // Route Request
      switch (request.type) {
        case 'chat':
          const chatPayload = request.payload as ChatPayload;
          data = await this.orchestrator.routeChat(chatPayload.message, memoryContext);
          break;
        case 'voice':
          data = await this.orchestrator.processVoice((request.payload as VoicePayload).audioBuffer);
          break;
        case 'workflow':
          data = await this.orchestrator.executeWorkflow((request.payload as WorkflowPayload).workflowId);
          break;
        case 'pattern':
          data = await this.patternIntel.detect((request.payload as PatternPayload).stream);
          break;
        case 'graph':
          data = await this.knowledgeGraph.queryOrUpdate((request.payload as GraphPayload).query);
          break;
        default:
          throw new Error(`Unknown request type: ${request.type}`);
      }

      // Auto-Knowledge Extraction (Async)
    this.backgroundKnowledgeUpdate(request, data, startTime);

    } catch (error) {
      console.error('[UnifiedAIWorker] Error:', error);
      return {
        success: false,
        data: error instanceof Error ? error.message : 'Unknown strict error',
        latencyMs: Date.now() - startTime,
      };
    }

    return {
      success: true,
      data,
      latencyMs: Date.now() - startTime,
    };
  }

  private async retrieveContext(userId: string): Promise<{ lastAgent: AgentPersona; userId: string }> {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve({ lastAgent: 'GENERAL', userId });
        }, 5);
    });
  }

  private backgroundKnowledgeUpdate(request: AIRequest, responseData: unknown, timestamp: number): void {
    setTimeout(async () => {
        try {
            // Explicitly inject timestamp into the knowledge extraction interaction
            const interaction = { 
                input: request, 
                output: responseData,
                timestamp 
            };
            await this.knowledgeGraph.extractAndStore(interaction);
        } catch (e) {
            console.error("Background knowledge update failed", e);
        }
    }, 0);
  }
}
