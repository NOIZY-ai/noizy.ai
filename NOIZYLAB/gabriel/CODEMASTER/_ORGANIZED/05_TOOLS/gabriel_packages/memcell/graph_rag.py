# 🤖 SYSTEM FILE: graph_rag.py
# Optimized by Healer Drone
# NO DEPENDENCIES. PURE PYTHON. ZERO LATENCY.

import json
import hashlib
import threading
import shutil
import queue
from pathlib import Path
from typing import List, Dict, Any, Optional, Set

class SimpleGraph:
    """ Light-weight directed graph using dicts """
    def __init__(self):
        # Nodes: {id: data_dict}
        self.nodes_data = {}
        # Edges: {source_id: {target_id: {relation: ...}}}
        self.adj = {}
    
    def add_node(self, node_id, **attr):
        if node_id not in self.nodes_data:
            self.nodes_data[node_id] = attr
            self.adj[node_id] = {}
        else:
            self.nodes_data[node_id].update(attr)

    def add_edge(self, u, v, **attr):
        if u not in self.nodes_data: self.add_node(u)
        if v not in self.nodes_data: self.add_node(v)
        
        if v not in self.adj[u]:
            self.adj[u][v] = attr
        else:
            self.adj[u][v].update(attr)

    def nodes(self, data=False):
        if data:
            return self.nodes_data.items()
        return self.nodes_data.keys()

    def to_dict(self):
        return {
            "nodes": [{"id": k, **v} for k,v in self.nodes_data.items()],
            "links": [{"source": u, "target": v, **attr} for u, neighbors in self.adj.items() for v, attr in neighbors.items()]
        }

    def from_dict(self, data):
        for node in data.get("nodes", []):
            nid = node.pop("id", None)
            if nid: self.add_node(nid, **node)
        for link in data.get("links", []):
            src = link.pop("source", None)
            tgt = link.pop("target", None)
            if src and tgt: self.add_edge(src, tgt, **link)

class GraphRAG:
    """
    GABRIEL MEMCELL v4.2 - GraphRAG Manager (Zero Dep)
    M2 Ultra Optimized: Pure Python Dict Graph.
    """
    def __init__(self, db_path: str = "./data/knowledge_graph.json"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = threading.RLock()
        self.graph = SimpleGraph()
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
                claim=cell.get("claim", cell.get("content", "")[:50]),
                confidence=cell.get("confidence", 1.0)
            )

            # 2. Extract & Link Entities
            entities = cell.get("entities", [])
            if not entities:
                if cell.get("subject") and cell.get("subject") != "General":
                    entities.append(cell.get("subject"))
                if cell.get("author"):
                    entities.append(cell.get("author"))
                entities.extend(cell.get("tags", []))

            for entity in entities:
                clean_ent = str(entity).strip()
                if not clean_ent: continue
                
                entity_id = f"ent_{hashlib.sha256(clean_ent.lower().encode()).hexdigest()[:8]}"
                self.graph.add_node(entity_id, label=clean_ent, type="entity")
                self.graph.add_edge(cell_id, entity_id, relation="MENTIONS")

            # 3. Overlaps
            overlaps = cell.get("overlap", [])
            for ov_id in overlaps:
                self.graph.add_edge(cell_id, ov_id, relation="OVERLAPS_WITH")

        if auto_save:
            self.background_save()

    def query_subgraph(self, topic: str, depth: int = 2) -> List[Any]:
        """ BFS Traversal """
        with self.lock:
            topic_lower = topic.lower()
            candidates = []
            
            for n, d in self.graph.nodes(data=True):
                label = d.get('label', '')
                claim = d.get('claim', '')
                if topic_lower in str(label).lower() or topic_lower in str(claim).lower():
                    candidates.append(n)
            
            if not candidates:
                return []

            # BFS
            result_nodes = set()
            visited = set()
            q = queue.Queue()
            
            for start in candidates:
                q.put((start, 0))
                visited.add(start)
                result_nodes.add(start)

            while not q.empty():
                curr, d = q.get()
                if d >= depth: continue
                
                # Get neighbors
                neighbors = self.graph.adj.get(curr, {})
                for neighbor in neighbors:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        result_nodes.add(neighbor)
                        q.put((neighbor, d + 1))

            return list(result_nodes)

    def background_save(self):
        threading.Thread(target=self.save, daemon=True).start()

    def save(self):
        with self.lock:
            data = self.graph.to_dict()
        
        temp_path = self.db_path.with_suffix('.tmp')
        try:
            with open(temp_path, "w") as f:
                json.dump(data, f, indent=0)
            shutil.move(str(temp_path), str(self.db_path))
        except Exception as e:
            print(f"GraphRAG Save Error: {e}")

    def load(self):
        with self.lock:
            if self.db_path.exists():
                try:
                    with open(self.db_path, "r") as f:
                        data = json.load(f)
                        self.graph.from_dict(data)
                except Exception as e:
                    print(f"GraphRAG Load Error: {e} - Starting fresh.")
                    self.graph = SimpleGraph()
            else:
                 self.graph = SimpleGraph()

_graph_instance = None

def get_graph_rag():
    global _graph_instance
    if _graph_instance is None:
        base_path = Path(__file__).parent.parent.parent / "data" / "knowledge_graph.json"
        _graph_instance = GraphRAG(str(base_path))
    return _graph_instance

if __name__ == "__main__":
    rag = GraphRAG("./test_graph.json")
    rag.add_memcell({"id": "test_1", "content": "Zero Dependency Graph"})
    print(f"Graph Nodes: {len(rag.graph.nodes_data)}")
    rag.save()
