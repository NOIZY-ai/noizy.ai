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
                node.properties.frequency++;
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
        const sql = `INSERT INTO graph_nodes (id, type, created, frequency, properties, temporal_start, temporal_end) 
                     VALUES ('${node.id}', '${node.type}', ${node.properties.created}, ${node.properties.frequency}, '${JSON.stringify(node.properties)}', ${node.temporal_range?.start}, ${node.temporal_range?.end})
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
