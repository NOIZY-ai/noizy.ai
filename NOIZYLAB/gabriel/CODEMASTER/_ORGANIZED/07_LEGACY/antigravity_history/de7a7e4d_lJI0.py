import networkx as nx
import json
import hashlib
import threading
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional

class GraphRAG:
    """
    GABRIEL MEMCELL v4.1 - GraphRAG Manager (Turbo Optimized)
    Implements Knowledge Graph + Vector relationships.
    M2 Ultra Optimized: 
    - In-memory NetworkX for zero-latency queries.
    - Asynchronous, atomic JSON persistence to prevent blocking.
    - Thread-safe operations.
    """
    def __init__(self, db_path: str = "./data/knowledge_graph.json"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = threading.RLock()
        self.graph = nx.MultiDiGraph()
        self.load()

    def add_memcell(self, cell: Dict[str, Any], auto_save: bool = True):
        """ Ingests a MemCell ensuring atomic nodes and edge relationships """
        cell_id = cell.get("id")
        if not cell_id:
            return

        with self.lock:
            # 1. Add Node (The MemCell Itself)
            self.graph.add_node(
                cell_id,
                type=cell.get("type", "fact"),
                claim=cell.get("claim", cell.get("content", "")[:50]), # Fallback to content snippet
                confidence=cell.get("confidence", 1.0)
            )

            # 2. Extract & Link Entities (The "Graph" part)
            # Use 'tags' and 'subject' as entities if 'entities' list is missing
            entities = cell.get("entities", [])
            
            # Auto-extract from tags/subject if not explicit entities
            if not entities:
                if cell.get("subject") and cell.get("subject") != "General":
                    entities.append(cell.get("subject"))
                if cell.get("author"):
                    entities.append(cell.get("author"))
                # Add tags as entities
                entities.extend(cell.get("tags", []))

            for entity in entities:
                 # Normalize entity ID
                clean_ent = str(entity).strip()
                if not clean_ent: continue
                
                entity_id = f"ent_{hashlib.sha256(clean_ent.lower().encode()).hexdigest()[:8]}"
                self.graph.add_node(entity_id, label=clean_ent, type="entity")
                self.graph.add_edge(cell_id, entity_id, relation="MENTIONS")

            # 3. Link Evidence sources / Overlaps
            overlaps = cell.get("overlap", [])
            for ov_id in overlaps:
                self.graph.add_edge(cell_id, ov_id, relation="OVERLAPS_WITH")

        if auto_save:
            self.background_save()

    def query_subgraph(self, topic: str, depth: int = 2) -> List[Any]:
        """ Returns a sub-graph related to a topic (Keyword search on nodes) """
        with self.lock:
            # Optimize: Generator expression + lower case set for instant lookup
            topic_lower = topic.lower()
            candidates = []
            
            for n, d in self.graph.nodes(data=True):
                # Search in label (entity) or claim (fact)
                label = d.get('label', '')
                claim = d.get('claim', '')
                if topic_lower in str(label).lower() or topic_lower in str(claim).lower():
                    candidates.append(n)
            
            if not candidates:
                return []

            # Traverse
            result_nodes = set()
            for start_node in candidates:
                 # BFS is fast for small depths
                 try:
                     sub = nx.bfs_tree(self.graph, start_node, depth_limit=depth)
                     result_nodes.update(sub.nodes())
                 except Exception:
                     continue # Handle potential disconnected components or errors efficiently

            return list(result_nodes)

    def background_save(self):
        """ Fires a non-blocking save operation """
        threading.Thread(target=self.save, daemon=True).start()

    def save(self):
        """ Atomic Save: Write to temp, then move. """
        with self.lock:
            # Convert to JSON-serializable format
            data = nx.node_link_data(self.graph)
        
        # Write to temp file first (I/O heavy part outside lock if possible, 
        # but for consistency we need the snapshot. NetworkX node_link_data is fast.)
        temp_path = self.db_path.with_suffix('.tmp')
        try:
            with open(temp_path, "w") as f:
                json.dump(data, f, indent=0) # Indent 0 for speed/minification
            
            # Atomic move
            shutil.move(str(temp_path), str(self.db_path))
        except Exception as e:
            print(f"GraphRAG Save Error: {e}")

    def load(self):
        with self.lock:
            if self.db_path.exists():
                try:
                    with open(self.db_path, "r") as f:
                        data = json.load(f)
                        self.graph = nx.node_link_graph(data)
                except Exception as e:
                    print(f"GraphRAG Load Error: {e} - Starting fresh graph.")
                    self.graph = nx.MultiDiGraph()
            else:
                 self.graph = nx.MultiDiGraph()

# Singleton Instance for sharing state if needed
_graph_instance = None

def get_graph_rag():
    global _graph_instance
    if _graph_instance is None:
        # Resolve correct path relative to GABRIEL_CORE
        # Assuming we are running from root or similar
        base_path = Path(__file__).parent.parent.parent / "data" / "knowledge_graph.json"
        _graph_instance = GraphRAG(str(base_path))
    return _graph_instance

if __name__ == "__main__":
    # Test
    rag = GraphRAG("./test_graph.json")
    rag.add_memcell({
        "id": "mc_test_001",
        "type": "fact",
        "content": "Gabriel runs on M2 Ultra.",
        "tags": ["Gabriel", "M2 Ultra", "Apple Silicon"],
        "overlap": []
    })
    print(f"Graph Nodes: {len(rag.graph.nodes)}")
    rag.save()
    print("GraphRAG Index Updated.")
