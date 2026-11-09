/**
 * KNOWLEDGE_GRAPH_AI.ts
 *
 * Description:
 * Auto entity extraction, relationship mapping, graph queries.
 * Self-building knowledge base that grows with every interaction.
 */

interface GraphNode {
    id: string;
    type: string;
    properties: Record<string, any>;
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
        // Cypher-like or simple query parser
        if (query.startsWith('CREATE')) {
            return this.addNodeFromQuery(query);
        }
        return this.findRelated(query);
    }

    public async extractAndStore(interaction: { input: any, output: any }): Promise<void> {
        // NLP extraction logic (NER -> Relation Extraction -> Graph Insert)
        const content = JSON.stringify(interaction);
        const entities = this.mockNER(content);
        
        entities.forEach(e => {
            // Create or update node
            if (!this.nodes.has(e)) {
                this.nodes.set(e, { id: e, type: 'concept', properties: { created: Date.now(), frequency: 1 } });
            } else {
                const node = this.nodes.get(e)!;
                node.properties.frequency++;
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

    private mockNER(text: string): string[] {
        // Simple regex-based entity extraction for prototype
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
        const node = { id, type: 'manual', properties: { query: q }};
        this.nodes.set(id, node);
        return node;
    }

    private findRelated(term: string): GraphNode[] {
        // BFS/DFS or vector similarity search
        return Array.from(this.nodes.values()).slice(0, 5);
    }
}
