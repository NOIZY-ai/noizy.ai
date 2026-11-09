import { AiOrchestration } from './AI_ORCHESTRATION';
import { PatternIntelligence } from './PATTERN_INTELLIGENCE';
import { KnowledgeGraphAI } from './KNOWLEDGE_GRAPH_AI';

/**
 * UNIFIED_AI_WORKER.ts
 *
 * Description:
 * One API endpoint for all AI interaction. Handles Chat, Voice, Workflows,
 * Pattern Recognition, and Knowledge Graph updates.
 *
 * deployment: "deploy and forget"
 */

export interface AIRequest {
  type: 'chat' | 'voice' | 'workflow' | 'pattern' | 'graph';
  payload: any;
  context?: any;
  userId: string;
}

export interface AIResponse {
  success: boolean;
  data: any;
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
    console.log(`[UnifiedAIWorker] Processing request type: ${request.type}`);

    let data: any = null;

    try {
      // Parallel Execution: Proactive Checks + Memory Retrieval
      // We don't wait for one to finish before starting the other.
      const [_, memoryContext] = await Promise.all([
        this.patternIntel.analyzeContext(request.context),
        this.retrieveContext(request.userId)
      ]);

      // 3. Route Request
      switch (request.type) {
        case 'chat':
          // Pass context to router
          data = await this.orchestrator.routeChat(request.payload, memoryContext);
          break;
        case 'voice':
          data = await this.orchestrator.processVoice(request.payload);
          break;
        case 'workflow':
          data = await this.orchestrator.executeWorkflow(request.payload);
          break;
        case 'pattern':
          data = await this.patternIntel.detect(request.payload);
          break;
        case 'graph':
          data = await this.knowledgeGraph.queryOrUpdate(request.payload);
          break;
        default:
          throw new Error(`Unknown request type: ${request.type}`);
      }

      // 3. Auto-Knowledge Extraction (Async)
      this.backgroundKnowledgeUpdate(request, data);

    } catch (error) {
      console.error('[UnifiedAIWorker] Error:', error);
      return {
        success: false,
        data: error instanceof Error ? error.message : 'Unknown error',
        latencyMs: Date.now() - startTime,
      };
    }

    return {
      success: true,
      data,
      latencyMs: Date.now() - startTime,
    };
  }

  private async retrieveContext(userId: string): Promise<any> {
    // Simulating async DB/Cache call (e.g., KV or D1)
    // In a real scenario, this happens in parallel with pattern analysis
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve({ lastAgent: 'GENERAL', userId });
        }, 5); // 5ms simulated network latency
    });
  }

  private async backgroundKnowledgeUpdate(request: AIRequest, responseData: any) {
    // Fire and forget, don't block response
    setTimeout(async () => {
        try {
            await this.knowledgeGraph.extractAndStore({ input: request, output: responseData });
        } catch (e) {
            console.error("Background knowledge update failed", e);
        }
    }, 0);
  }
}

// Entry point for Cloudflare Worker or simple server
const worker = new UnifiedAIWorker();
export default worker;
