import networkx as nx
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Any

class GraphRAG:
    """
    GABRIEL MEMCELL v4.0 - GraphRAG Manager
    Implements Knowledge Graph + Vector relationships.
    M2 Ultra Optimized: Uses in-memory NetworkX for speed + JSON persistence.
    Future: Connects to Neo4j/ArangoDB via 'connector' method.
    """
    def __init__(self, db_path: str = "./data/knowledge_graph.json"):
        self.graph = nx.MultiDiGraph()
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.load()

    def add_memcell(self, cell: Dict[str, Any]):
        """ Ingests a MemCell ensuring atomic nodes and edge relationships """
        cell_id = cell.get("id")
        if not cell_id:
            return

        # 1. Add Node (The MemCell Itself)
        self.graph.add_node(
            cell_id, 
            type=cell.get("type", "fact"),
            claim=cell.get("claim", ""),
            confidence=cell.get("confidence", 0.0)
        )

        # 2. Extract & Link Entities (The "Graph" part)
        # "Gabriel" -> [HAS_MEMORY] -> "MemCell_123"
        entities = cell.get("entities", [])
        for entity in entities:
             # Normalize entity ID
            entity_id = f"ent_{hashlib.sha256(entity.lower().encode()).hexdigest()[:8]}"
            self.graph.add_node(entity_id, label=entity, type="entity")
            self.graph.add_edge(cell_id, entity_id, relation="MENTIONS")

        # 3. Link Evidence sources
        provenance = cell.get("provenance", {})
        for src_id in provenance.get("source_ids", []):
            self.graph.add_edge(cell_id, src_id, relation="DERIVED_FROM")

    def query_subgraph(self, topic: str, depth: int = 2):
        """ Returns a sub-graph related to a topic (Keyword search on nodes) """
        # Naive implementation for demo: find closest node matching string
        # Real implementation: Vector Similarity Search -> Graph Traversal
        candidates = [n for n, d in self.graph.nodes(data=True) if topic.lower() in str(d).lower()]
        if not candidates:
            return []
        
        # Traverse
        result_nodes = set()
        for start_node in candidates:
             sub = nx.bfs_tree(self.graph, start_node, depth_limit=depth)
             result_nodes.update(sub.nodes())
        
        return list(result_nodes)

    def save(self):
        data = nx.node_link_data(self.graph)
        with open(self.db_path, "w") as f:
            json.dump(data, f, indent=2)

    def load(self):
        if self.db_path.exists():
            with open(self.db_path, "r") as f:
                data = json.load(f)
                self.graph = nx.node_link_graph(data)

if __name__ == "__main__":
    # Test
    rag = GraphRAG()
    rag.add_memcell({
        "id": "mc_test_001",
        "type": "fact",
        "claim": "Gabriel runs on M2 Ultra.",
        "entities": ["Gabriel", "M2 Ultra", "Apple Silicon"],
        "provenance": {"source_ids": ["src_blue_01"]}
    })
    rag.save()
    print("GraphRAG Index Updated.")
