/**
 * KNOWLEDGE_GRAPH_AI.ts
 *
 * Description:
 * Auto entity extraction, relationship mapping, graph queries.
 * Self-building knowledge base that grows with every interaction.
 *
 * GOD MODE: ENABLED
 * STRICT MODE: ENABLED
 */

export interface TemporalRange {
    start: number;
    end: number;
}

export interface GraphNode {
    id: string;
    type: string;
    properties: Record<string, unknown>;
    temporal_range?: TemporalRange;
    created: number;
    updated: number;
}

export interface GraphEdge {
    id: string;
    source: string;
    target: string;
    relationship: string;
    weight: number;
    created: number;
}

export interface InteractionPayload {
    input: unknown;
    output: unknown;
    timestamp?: number;
    userId?: string;
}

export interface QueryResult {
    nodes: GraphNode[];
    edges: GraphEdge[];
    metadata?: Record<string, unknown>;
}

// Entity extraction patterns
const ENTITY_PATTERNS: Array<{ pattern: RegExp; type: string }> = [
    // Projects
    { pattern: /Project\s+(\w+)/gi, type: 'PROJECT' },
    // Technologies
    { pattern: /(TypeScript|JavaScript|Python|Swift|Rust|Go|Java|C\+\+)/gi, type: 'TECHNOLOGY' },
    // AI Systems
    { pattern: /(GPT-4|GPT-4o|Claude|Gemini|LLaMA|Mistral)/gi, type: 'AI_MODEL' },
    { pattern: /(OpenAI|Anthropic|Google|Meta|Microsoft)/gi, type: 'COMPANY' },
    // Voice Technologies
    { pattern: /(TTS|Text-to-Speech|Whisper|Voice Engine)/gi, type: 'VOICE_TECH' },
    // APIs and Services
    { pattern: /(Realtime API|REST API|GraphQL|WebSocket)/gi, type: 'API' },
    // Concepts
    { pattern: /(latency|multimodal|embedding|vector)/gi, type: 'CONCEPT' },
];

export class KnowledgeGraphAI {
    private nodes: Map<string, GraphNode>;
    private edges: Map<string, GraphEdge>;
    private edgeIndex: Map<string, string[]>; // node -> edge ids

    constructor() {
        this.nodes = new Map();
        this.edges = new Map();
        this.edgeIndex = new Map();
    }

    public async queryOrUpdate(query: string): Promise<QueryResult> {
        // Temporal Overlap Query
        if (query.startsWith("overlap:")) {
            const [, rangeStr] = query.split(":");
            const [start, end] = rangeStr.split(",").map(Number);
            const overlaps = this.findTemporalOverlaps({ start, end });
            return { nodes: overlaps, edges: [] };
        }

        // Entity search
        if (query.startsWith("find:")) {
            const [, searchTerm] = query.split(":");
            const nodes = this.searchNodes(searchTerm);
            const edges = this.getEdgesForNodes(nodes.map(n => n.id));
            return { nodes, edges };
        }

        // Relationship query
        if (query.startsWith("related:")) {
            const [, nodeId] = query.split(":");
            const related = this.getRelatedNodes(nodeId);
            return related;
        }

        // Stats query
        if (query === "stats") {
            return {
                nodes: [],
                edges: [],
                metadata: {
                    nodeCount: this.nodes.size,
                    edgeCount: this.edges.size,
                    types: this.getNodeTypes()
                }
            };
        }

        // Default: Natural language processing
        const entities = this.extractEntities(query);
        for (const entity of entities) {
            this.addOrUpdateNode(entity.text, entity.type);
        }

        return {
            nodes: entities.map(e => this.nodes.get(e.text)!).filter(Boolean),
            edges: [],
            metadata: { extracted: entities.length }
        };
    }

    public async extractAndStore(interaction: InteractionPayload): Promise<void> {
        const content = JSON.stringify(interaction);
        const timestamp = interaction.timestamp || Date.now();

        // Extract entities
        const entities = this.extractEntities(content);

        for (const entity of entities) {
            const node = this.addOrUpdateNode(entity.text, entity.type, {
                lastInteraction: timestamp
            });

            if (node.temporal_range) {
                node.temporal_range.end = timestamp;
            }
        }

        // Create co-occurrence edges
        for (let i = 0; i < entities.length; i++) {
            for (let j = i + 1; j < entities.length; j++) {
                this.addOrUpdateEdge(
                    entities[i].text,
                    entities[j].text,
                    'CO_OCCURRENCE'
                );
            }
        }

        console.log(`[KnowledgeGraph] Extracted ${entities.length} entities. Graph Size: ${this.nodes.size} nodes, ${this.edges.size} edges.`);
    }

    private extractEntities(text: string): Array<{ text: string; type: string }> {
        const entities: Array<{ text: string; type: string }> = [];
        const seen = new Set<string>();

        for (const { pattern, type } of ENTITY_PATTERNS) {
            const matches = text.matchAll(new RegExp(pattern.source, 'gi'));
            for (const match of matches) {
                const entityText = match[1] || match[0];
                const normalized = entityText.toUpperCase();
                if (!seen.has(normalized)) {
                    seen.add(normalized);
                    entities.push({ text: entityText, type });
                }
            }
        }

        // Default entity for non-empty text
        if (entities.length === 0 && text.length > 20) {
            entities.push({ text: 'General_Interaction', type: 'INTERACTION' });
        }

        return entities;
    }

    private addOrUpdateNode(id: string, type: string, properties: Record<string, unknown> = {}): GraphNode {
        const existing = this.nodes.get(id);
        const now = Date.now();

        if (existing) {
            existing.updated = now;
            existing.properties = { ...existing.properties, ...properties };
            (existing.properties as { frequency: number }).frequency =
                ((existing.properties as { frequency?: number }).frequency || 0) + 1;
            return existing;
        }

        const node: GraphNode = {
            id,
            type,
            properties: { frequency: 1, ...properties },
            temporal_range: { start: now, end: now },
            created: now,
            updated: now
        };

        this.nodes.set(id, node);
        return node;
    }

    private addOrUpdateEdge(source: string, target: string, relationship: string): GraphEdge {
        const edgeId = `${source}:${relationship}:${target}`;
        const existing = this.edges.get(edgeId);
        const now = Date.now();

        if (existing) {
            existing.weight++;
            return existing;
        }

        const edge: GraphEdge = {
            id: edgeId,
            source,
            target,
            relationship,
            weight: 1,
            created: now
        };

        this.edges.set(edgeId, edge);

        // Update index
        this.addToEdgeIndex(source, edgeId);
        this.addToEdgeIndex(target, edgeId);

        return edge;
    }

    private addToEdgeIndex(nodeId: string, edgeId: string): void {
        const existing = this.edgeIndex.get(nodeId) || [];
        existing.push(edgeId);
        this.edgeIndex.set(nodeId, existing);
    }

    public findTemporalOverlaps(range: TemporalRange): GraphNode[] {
        const overlaps: GraphNode[] = [];

        this.nodes.forEach(node => {
            if (node.temporal_range) {
                // Check intersection: (StartA <= EndB) and (EndA >= StartB)
                if (node.temporal_range.start <= range.end &&
                    node.temporal_range.end >= range.start) {
                    overlaps.push(node);
                }
            }
        });

        return overlaps;
    }

    private searchNodes(term: string): GraphNode[] {
        const lowerTerm = term.toLowerCase();
        return Array.from(this.nodes.values()).filter(node =>
            node.id.toLowerCase().includes(lowerTerm) ||
            node.type.toLowerCase().includes(lowerTerm)
        );
    }

    private getEdgesForNodes(nodeIds: string[]): GraphEdge[] {
        const edgeSet = new Set<string>();

        for (const nodeId of nodeIds) {
            const edgeIds = this.edgeIndex.get(nodeId) || [];
            for (const edgeId of edgeIds) {
                edgeSet.add(edgeId);
            }
        }

        return Array.from(edgeSet).map(id => this.edges.get(id)!).filter(Boolean);
    }

    private getRelatedNodes(nodeId: string): QueryResult {
        const edgeIds = this.edgeIndex.get(nodeId) || [];
        const edges = edgeIds.map(id => this.edges.get(id)!).filter(Boolean);

        const relatedIds = new Set<string>();
        for (const edge of edges) {
            if (edge.source !== nodeId) relatedIds.add(edge.source);
            if (edge.target !== nodeId) relatedIds.add(edge.target);
        }

        const nodes = Array.from(relatedIds).map(id => this.nodes.get(id)!).filter(Boolean);

        return { nodes, edges };
    }

    private getNodeTypes(): Record<string, number> {
        const types: Record<string, number> = {};

        this.nodes.forEach(node => {
            types[node.type] = (types[node.type] || 0) + 1;
        });

        return types;
    }

    public getNode(id: string): GraphNode | undefined {
        return this.nodes.get(id);
    }

    public getAllNodes(): GraphNode[] {
        return Array.from(this.nodes.values());
    }

    public getAllEdges(): GraphEdge[] {
        return Array.from(this.edges.values());
    }

    public clear(): void {
        this.nodes.clear();
        this.edges.clear();
        this.edgeIndex.clear();
    }

    public export(): { nodes: GraphNode[]; edges: GraphEdge[] } {
        return {
            nodes: this.getAllNodes(),
            edges: this.getAllEdges()
        };
    }

    public import(data: { nodes: GraphNode[]; edges: GraphEdge[] }): void {
        for (const node of data.nodes) {
            this.nodes.set(node.id, node);
        }
        for (const edge of data.edges) {
            this.edges.set(edge.id, edge);
            this.addToEdgeIndex(edge.source, edge.id);
            this.addToEdgeIndex(edge.target, edge.id);
        }
    }
}
