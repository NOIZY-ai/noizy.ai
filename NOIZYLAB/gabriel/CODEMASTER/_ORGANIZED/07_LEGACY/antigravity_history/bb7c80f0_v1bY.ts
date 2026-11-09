/**
 * KNOWLEDGE_GRAPH_AI.ts
 *
 * Description:
 * Auto entity extraction, relationship mapping, graph queries.
 * Self-building knowledge base that grows with every interaction.
 */

interface TemporalRange {
    start: number;
    end: number;
}

interface GraphNode {
    id: string;
    type: 'concept' | 'event' | 'subject';
    properties: {
        created: number;
        frequency: number;
        [key: string]: any;
    };
    temporal_range?: TemporalRange;
}

interface GraphEdge {
    source: string;
    target: string;
    relationship: string;
    weight: number;
}

export class KnowledgeGraphAI {
    private nodes: Map<string, GraphNode> = new Map();
    private edges: GraphEdge[] = [];

    public async queryOrUpdate(query: string): Promise<any> {
        if (query.startsWith('CREATE')) {
            return this.addNodeFromQuery(query);
        }
        return this.findRelated(query);
    }

    public async extractAndStore(interaction: { input: any, output: any }): Promise<void> {
        const content = JSON.stringify(interaction);
        const timestamp = Date.now();
        
        // Extract Entities (Subjects)
        const entities = this.mockNER(content);
        
        entities.forEach(e => {
            if (!this.nodes.has(e)) {
                this.nodes.set(e, { 
                    id: e, 
                    type: 'subject', 
                    properties: { created: timestamp, frequency: 1 },
                    temporal_range: { start: timestamp, end: timestamp } // Point-in-time
                });
            } else {
                const node = this.nodes.get(e)!;
                node.properties.frequency++;
                // Extend temporal range to cover latest occurrence
                if (node.temporal_range) {
                    node.temporal_range.end = timestamp;
                }
            }
        });

        // Link entities (Clique)
        for (let i = 0; i < entities.length; i++) {
            for (let j = i + 1; j < entities.length; j++) {
                this.edges.push({
                    source: entities[i],
                    target: entities[j],
                    relationship: 'CO_OCCURRENCE',
                    weight: 1
                });
            }
        }
        
        console.log(`[KnowledgeGraph] Extracted ${entities.length} entities. Graph Size: ${this.nodes.size} nodes.`);
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
        const entities: string[] = [];
        const potential = text.match(/\b(User|Code|Project|Timeline|Bug|Feature|Deploy|API|Database)\b/gi);
        if (potential) {
            potential.forEach(p => {
                const normalized = p.toUpperCase();
                if (!entities.includes(normalized)) entities.push(normalized);
            });
        }
        return entities;
    }

    private addNodeFromQuery(q: string): GraphNode {
        const id = `node_${Date.now()}`;
        const node: GraphNode = { 
            id, 
            type: 'event', 
            properties: { created: Date.now(), frequency: 1, query: q },
            temporal_range: { start: Date.now(), end: Date.now() }
        };
        this.nodes.set(id, node);
        return node;
    }

    private findRelated(term: string): GraphNode[] {
        return Array.from(this.nodes.values()).slice(0, 5);
    }
}
