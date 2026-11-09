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
    properties: Record<string, unknown>; // Safer than any
    temporal_range?: TemporalRange;
}

export interface GraphEdge {
    source: string;
    target: string;
    relationship: string;
    weight: number;
}

export interface InteractionPayload {
    input: unknown;
    output: unknown;
    timestamp?: number;
}

export class KnowledgeGraphAI {
    private nodes: Map<string, GraphNode>;
    private edges: GraphEdge[];

    constructor() {
        this.nodes = new Map();
        this.edges = [];
    }

    public async queryOrUpdate(query: string): Promise<{ result: string | GraphNode[] }> {
        // Temporal Overlap Query
        if (query.startsWith("overlap:")) {
             const [_, rangeStr] = query.split(":");
             const [start, end] = rangeStr.split(",").map(Number);
             const overlaps = this.findTemporalOverlaps({ start, end });
             return { result: overlaps };
        }

        // Natural Language to Graph Query (Mock)
        if (query.includes("who")) {
            return { result: "Searching graph for entities..." };
        }
        return { result: "Graph updated." };
    }

    public async extractAndStore(interaction: InteractionPayload): Promise<void> {
        const content = JSON.stringify(interaction);
        const timestamp = interaction.timestamp || Date.now();
        
        if (content.includes("pattern") || content.includes("stream")) {
            // Feedback Loop: If interaction is a Pattern detection, log the pattern in the graph
            try {
               interface PatternInput { payload: unknown; }
               interface PatternOutput { signature: string; confidence: number; }
               const payload = (interaction.input as PatternInput).payload;
                if (payload && Array.isArray(interaction.output)) {
                    const patterns = interaction.output as PatternOutput[];
                    patterns.forEach(p => {
                         const pNodeId = `PATTERN:${p.signature}`;
                         if (!this.nodes.has(pNodeId)) {
                             this.nodes.set(pNodeId, { id: pNodeId, type: 'PATTERN', properties: { confidence: p.confidence, frequency: 1 }, temporal_range: { start: timestamp, end: timestamp } });
                         } else {
                             const pNode = this.nodes.get(pNodeId)!;
                             (pNode.properties as { frequency: number }).frequency++;
                         }
                    });
                }
            } catch (e) { /* ignore pattern extract error */ }
        }

        // Extract Entities (Subjects)
        const entities = this.mockNER(content);
        
        for (const e of entities) {
            let node = this.nodes.get(e);
            if (!node) {
                node = { 
                    id: e, 
                    type: 'subject', 
                    properties: { created: timestamp, frequency: 1 },
                    temporal_range: { start: timestamp, end: timestamp }
                };
                this.nodes.set(e, node);
            } else {
                const props = node.properties as { frequency: number }; // Type assertion safe here due to initialization
                props.frequency++;
                if (node.temporal_range) {
                    node.temporal_range.end = timestamp;
                }
            }
            // PERSISTENCE (Gabriel's Ingestion)
            await this.persistNode(node);
        }

        // Link entities (Clique)
        for (let i = 0; i < entities.length; i++) {
            for (let j = i + 1; j < entities.length; j++) {
                this.edges.push({
                    source: entities[i],
                    target: entities[j],
                    relationship: 'CO_OCCURRENCE',
                    weight: 1
                });
                // Persist Edge
                await this.persistEdge(entities[i], entities[j], 'CO_OCCURRENCE');
            }
        }
        
        console.log(`[KnowledgeGraph] Extracted ${entities.length} entities. Graph Size: ${this.nodes.size} nodes.`);
    }

    private async persistNode(node: GraphNode): Promise<void> {
        // In a real generic class, we might not have 'env', so we simulate the SQL generation
        // for "Gabriel" to ingest later or for testing purposes.
        const created = (node.properties as { created?: number }).created || 0;
        const frequency = (node.properties as { created?: number; frequency?: number }).frequency || 0;

        const sql = `INSERT INTO graph_nodes (id, type, created, frequency, properties, temporal_start, temporal_end) 
                     VALUES ('${node.id}', '${node.type}', ${created}, ${frequency}, '${JSON.stringify(node.properties)}', ${node.temporal_range?.start}, ${node.temporal_range?.end})
                     ON CONFLICT(id) DO UPDATE SET frequency = frequency + 1, temporal_end = ${node.temporal_range?.end};`;
        // console.log('[DB_WRITE]', sql); // Silence for speed
    }

    private async persistEdge(source: string, target: string, rel: string): Promise<void> {
         const sql = `INSERT INTO graph_edges (source, target, relationship, weight)
                      VALUES ('${source}', '${target}', '${rel}', 1)
                      ON CONFLICT(source, target, relationship) DO UPDATE SET weight = weight + 1;`;
         // console.log('[DB_WRITE]', sql);
    }

    public findTemporalOverlaps(range: TemporalRange): GraphNode[] {
        const overlaps: GraphNode[] = [];
        this.nodes.forEach(node => {
            if (node.temporal_range) {
                // Check intersection: (StartA <= EndB) and (EndA >= StartB)
                if (node.temporal_range.start <= range.end && node.temporal_range.end >= range.start) {
                    overlaps.push(node);
                }
            }
        });
        return overlaps;
    }

    private mockNER(text: string): string[] {
        // Improved Regex-based NER for "Subject Matter" and "Entities"
        const entities = new Set<string>();
        
        // 1. Project/Code Terms
        const techTerms = text.match(/\b(TypeScript|Python|API|Database|D1|Worker|Deploy|Optimization|Latency|Graph|Node|Edge)\b/gi);
        if (techTerms) techTerms.forEach(t => entities.add(t.toUpperCase()));

        // 2. Specific Project Names (Contextual)
        if (text.match(/MC96/i)) entities.add("MC96_ECOUNIVERSE");
        if (text.match(/NoizyLab/i)) entities.add("NOIZYLAB");
        if (text.match(/God Mode/i)) entities.add("GOD_MODE");

        // 3. Dates/Times (Temporal)
        // Simple heuristic: "Phase X", "Year 202X"
        const phases = text.match(/Phase \d+/gi);
        if (phases) phases.forEach(p => entities.add(p.toUpperCase()));

        // 4. Default if empty
        if (entities.size === 0 && text.length > 10) {
            entities.add("GENERAL_INTERACTION");
        }

        return Array.from(entities);
    }
}
