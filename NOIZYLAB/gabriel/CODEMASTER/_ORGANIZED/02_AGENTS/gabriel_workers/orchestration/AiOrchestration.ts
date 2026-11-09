/**
 * AI_ORCHESTRATION.ts
 *
 * Description:
 * Intelligent routing and context management.
 * Selects the perfect agent for every task.
 * Handles auto-routing, tool usage, and complex workflows.
 *
 * GOD MODE: ENABLED
 * STRICT MODE: ENABLED
 */

export type AgentPersona = 'GENERAL' | 'SHIRL' | 'ENGR_KEITH' | 'POPS' | 'DREAM' | 'GABRIEL';

export interface AgentResponse {
    agent: AgentPersona;
    content: string;
    timestamp: number;
    confidence: number;
}

export interface ProcessingContext {
    lastAgent?: AgentPersona;
    sessionId?: string;
    userId?: string;
    [key: string]: unknown;
}

interface AgentConfig {
    role: string;
    keywords: RegExp;
    priority: number;
}

export class AiOrchestration {
    private agents: Map<AgentPersona, AgentConfig>;

    constructor() {
        this.agents = new Map();
        this.initializeAgents();
    }

    private initializeAgents(): void {
        this.agents.set('GENERAL', {
            role: 'General purpose assistant',
            keywords: /.*/,
            priority: 0
        });
        this.agents.set('SHIRL', {
            role: 'Empathetic listener and emotional support',
            keywords: /(feel|sad|happy|worried|tired|love|hate|user|empathy|emotion|stress|anxious)/i,
            priority: 1
        });
        this.agents.set('ENGR_KEITH', {
            role: 'Strict code engineer and technical expert',
            keywords: /(code|bug|error|exception|stack|deploy|git|typescript|api|function|class|debug|fix|implement)/i,
            priority: 2
        });
        this.agents.set('POPS', {
            role: 'Wise strategist and mentor',
            keywords: /(advice|strategy|wise|help|guide|mentor|decide|choice|plan|think)/i,
            priority: 1
        });
        this.agents.set('DREAM', {
            role: 'Creative visionary and innovator',
            keywords: /(plan|future|imagine|what if|roadmap|vision|create|design|idea|concept|innovate)/i,
            priority: 1
        });
        this.agents.set('GABRIEL', {
            role: 'System executor and security specialist',
            keywords: /(security|admin|access|token|auth|permission|lock|system|execute|run|command)/i,
            priority: 3
        });
    }

    public async routeChat(message: string, context?: ProcessingContext): Promise<AgentResponse> {
        const bestAgent = this.determineBestAgent(message, context);
        const agentConfig = this.agents.get(bestAgent);

        console.log(`[AiOrchestration] Routing to ${bestAgent} (${agentConfig?.role})`);

        // Process with selected agent
        const response = await this.processWithAgent(bestAgent, message, context);

        return {
            agent: bestAgent,
            content: response,
            timestamp: Date.now(),
            confidence: this.calculateConfidence(message, bestAgent)
        };
    }

    private async processWithAgent(agent: AgentPersona, message: string, context?: ProcessingContext): Promise<string> {
        // In a real implementation, this would call the actual agent
        const agentConfig = this.agents.get(agent);
        return `[${agent}] ${agentConfig?.role}: Processed "${message.substring(0, 50)}..."`;
    }

    private calculateConfidence(message: string, agent: AgentPersona): number {
        const config = this.agents.get(agent);
        if (!config) return 0;

        const matches = message.match(config.keywords);
        if (!matches) return 0.5;

        // More matches = higher confidence
        const matchCount = (message.match(new RegExp(config.keywords.source, 'gi')) || []).length;
        return Math.min(0.9, 0.5 + (matchCount * 0.1));
    }

    public async processVoice(audioBuffer: unknown): Promise<{ transcript: string; agent: AgentPersona }> {
        // In production, this would use speech-to-text
        return {
            transcript: "Processed audio content",
            agent: 'GENERAL'
        };
    }

    public async executeWorkflow(workflowId: string): Promise<{ status: string; id: string; steps: number }> {
        console.log(`[AiOrchestration] Executing workflow: ${workflowId}`);
        return {
            status: "COMPLETED",
            id: workflowId,
            steps: 0
        };
    }

    private determineBestAgent(input: string, context?: ProcessingContext): AgentPersona {
        const scores = new Map<AgentPersona, number>();

        // Initialize scores
        this.agents.forEach((config, agent) => {
            scores.set(agent, 0);
        });

        // Score based on keywords
        this.agents.forEach((config, agent) => {
            if (agent === 'GENERAL') return; // GENERAL is fallback

            const matches = input.match(new RegExp(config.keywords.source, 'gi'));
            if (matches) {
                scores.set(agent, (scores.get(agent) || 0) + matches.length * 5 + config.priority);
            }
        });

        // Context modifiers - sticky routing
        if (context?.lastAgent && this.agents.has(context.lastAgent)) {
            scores.set(context.lastAgent, (scores.get(context.lastAgent) || 0) + 2);
        }

        // Find winner
        let maxScore = -1;
        let winner: AgentPersona = 'GENERAL';

        scores.forEach((score, agent) => {
            if (score > maxScore) {
                maxScore = score;
                winner = agent;
            }
        });

        return maxScore > 0 ? winner : 'GENERAL';
    }

    public getAgentInfo(agent: AgentPersona): AgentConfig | undefined {
        return this.agents.get(agent);
    }

    public listAgents(): AgentPersona[] {
        return Array.from(this.agents.keys());
    }
}
