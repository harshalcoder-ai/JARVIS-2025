"""
JARVIS Feature Module: Advanced Memory System
Add this to your existing JARVIS project for cognitive architecture

Features:
- Working Memory (short-term)
- Long-term Memory (Vector DB)
- Episodic Memory (events)
- Knowledge Graph (relationships)
"""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field
import json
from pathlib import Path


@dataclass
class Memory:
    """Memory entry structure"""
    content: str
    timestamp: datetime
    memory_type: str  # working, episodic, semantic
    importance: float = 0.5
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'memory_type': self.memory_type,
            'importance': self.importance,
            'metadata': self.metadata
        }


class AdvancedMemorySystem:
    """
    Complete memory system with working, episodic, semantic, and procedural memory
    
    Usage:
        memory = AdvancedMemorySystem()
        await memory.initialize()
        
        # Store memory
        await memory.store("User prefers Python over Java", memory_type="semantic")
        
        # Retrieve relevant memories
        results = await memory.retrieve("programming languages")
    """
    
    def __init__(self, data_dir: str = "data/memory"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Working memory (short-term, in RAM)
        self.working_memory: List[Memory] = []
        self.working_memory_size = 20
        
        # Long-term storage
        self.episodic_memory: List[Memory] = []
        self.semantic_memory: Dict[str, Any] = {}
        self.procedural_memory: Dict[str, Any] = {}
        
        # Vector DB (optional, graceful fallback)
        self.vector_db = None
        self.use_vector_db = False
        
        # Knowledge graph (optional)
        self.knowledge_graph = None
        
    async def initialize(self):
        """Initialize memory system"""
        print("🧠 Initializing Advanced Memory System...")
        
        # Try to initialize Vector DB
        try:
            import chromadb
            self.vector_db = chromadb.Client()
            self.collection = self.vector_db.get_or_create_collection("jarvis_memory")
            self.use_vector_db = True
            print("   ✅ Vector Database (ChromaDB) initialized")
        except ImportError:
            print("   ⚠️  ChromaDB not installed - using basic memory")
            print("      Install with: pip install chromadb")
        
        # Try to initialize Knowledge Graph
        try:
            import networkx as nx
            self.knowledge_graph = nx.Graph()
            print("   ✅ Knowledge Graph initialized")
        except ImportError:
            print("   ⚠️  NetworkX not installed - knowledge graph disabled")
            print("      Install with: pip install networkx")
        
        # Load existing memories
        await self._load_memories()
        print("   ✅ Memory system ready")
    
    async def store(self, content: str, memory_type: str = "episodic", 
                   importance: float = 0.5, metadata: Dict = None) -> bool:
        """
        Store a memory
        
        Args:
            content: The content to remember
            memory_type: Type of memory (working, episodic, semantic, procedural)
            importance: How important this memory is (0.0 - 1.0)
            metadata: Additional metadata
            
        Returns:
            Success boolean
        """
        memory = Memory(
            content=content,
            timestamp=datetime.now(),
            memory_type=memory_type,
            importance=importance,
            metadata=metadata or {}
        )
        
        # Add to working memory
        self.working_memory.append(memory)
        if len(self.working_memory) > self.working_memory_size:
            # Move old memory to long-term if important
            old_memory = self.working_memory.pop(0)
            if old_memory.importance > 0.5:
                await self._move_to_long_term(old_memory)
        
        # Store in appropriate long-term memory
        if memory_type == "episodic":
            self.episodic_memory.append(memory)
        elif memory_type == "semantic":
            # Store facts/knowledge
            key = content.lower()[:50]  # Use first 50 chars as key
            self.semantic_memory[key] = {
                'content': content,
                'timestamp': memory.timestamp.isoformat(),
                'importance': importance
            }
        elif memory_type == "procedural":
            # Store how-to knowledge
            if 'task' in metadata:
                self.procedural_memory[metadata['task']] = content
        
        # Store in vector DB if available
        if self.use_vector_db:
            try:
                self.collection.add(
                    documents=[content],
                    ids=[str(datetime.now().timestamp())],
                    metadatas=[{
                        'type': memory_type,
                        'importance': importance,
                        'timestamp': memory.timestamp.isoformat()
                    }]
                )
            except Exception as e:
                print(f"   Vector DB error: {e}")
        
        # Save to disk periodically
        if len(self.episodic_memory) % 10 == 0:
            await self._save_memories()
        
        return True
    
    async def retrieve(self, query: str, limit: int = 5, 
                      memory_type: Optional[str] = None) -> List[Dict]:
        """
        Retrieve relevant memories
        
        Args:
            query: What to search for
            limit: Maximum number of results
            memory_type: Filter by memory type (optional)
            
        Returns:
            List of relevant memories
        """
        results = []
        
        # Search vector DB if available
        if self.use_vector_db:
            try:
                search_results = self.collection.query(
                    query_texts=[query],
                    n_results=limit
                )
                
                if search_results['documents']:
                    for i, doc in enumerate(search_results['documents'][0]):
                        results.append({
                            'content': doc,
                            'metadata': search_results['metadatas'][0][i] if search_results['metadatas'] else {},
                            'distance': search_results['distances'][0][i] if search_results['distances'] else 0
                        })
                    return results
            except Exception as e:
                print(f"   Vector search error: {e}")
        
        # Fallback: Simple keyword search
        query_lower = query.lower()
        
        # Search working memory
        for memory in self.working_memory:
            if query_lower in memory.content.lower():
                results.append({
                    'content': memory.content,
                    'type': memory.memory_type,
                    'timestamp': memory.timestamp.isoformat(),
                    'importance': memory.importance
                })
        
        # Search episodic memory
        for memory in self.episodic_memory[-50:]:  # Last 50 episodes
            if query_lower in memory.content.lower():
                results.append({
                    'content': memory.content,
                    'type': memory.memory_type,
                    'timestamp': memory.timestamp.isoformat(),
                    'importance': memory.importance
                })
        
        # Search semantic memory
        for key, value in self.semantic_memory.items():
            if query_lower in value['content'].lower():
                results.append({
                    'content': value['content'],
                    'type': 'semantic',
                    'timestamp': value['timestamp'],
                    'importance': value['importance']
                })
        
        # Sort by importance and limit
        results.sort(key=lambda x: x.get('importance', 0), reverse=True)
        return results[:limit]
    
    async def add_to_knowledge_graph(self, entity1: str, relationship: str, 
                                    entity2: str, metadata: Dict = None):
        """
        Add relationship to knowledge graph
        
        Args:
            entity1: First entity (e.g., "User")
            relationship: Relationship type (e.g., "prefers")
            entity2: Second entity (e.g., "Python")
            metadata: Additional data
        """
        if not self.knowledge_graph:
            return
        
        try:
            # Add nodes
            self.knowledge_graph.add_node(entity1, **({'type': 'entity'} | (metadata or {})))
            self.knowledge_graph.add_node(entity2, **({'type': 'entity'} | (metadata or {})))
            
            # Add edge with relationship
            self.knowledge_graph.add_edge(
                entity1, entity2, 
                relationship=relationship,
                timestamp=datetime.now().isoformat()
            )
            
            print(f"   📊 Knowledge Graph: {entity1} -{relationship}-> {entity2}")
        except Exception as e:
            print(f"   Knowledge graph error: {e}")
    
    async def query_knowledge_graph(self, entity: str) -> Dict:
        """Query knowledge graph for an entity"""
        if not self.knowledge_graph or entity not in self.knowledge_graph:
            return {}
        
        try:
            import networkx as nx
            
            # Get neighbors and relationships
            neighbors = list(self.knowledge_graph.neighbors(entity))
            relationships = []
            
            for neighbor in neighbors:
                edge_data = self.knowledge_graph.get_edge_data(entity, neighbor)
                relationships.append({
                    'entity': neighbor,
                    'relationship': edge_data.get('relationship', 'related'),
                    'timestamp': edge_data.get('timestamp', '')
                })
            
            return {
                'entity': entity,
                'relationships': relationships,
                'degree': self.knowledge_graph.degree(entity)
            }
        except Exception as e:
            print(f"   Query error: {e}")
            return {}
    
    def get_working_memory(self) -> List[Dict]:
        """Get current working memory contents"""
        return [m.to_dict() for m in self.working_memory]
    
    def get_memory_stats(self) -> Dict:
        """Get memory system statistics"""
        return {
            'working_memory_count': len(self.working_memory),
            'episodic_memory_count': len(self.episodic_memory),
            'semantic_memory_count': len(self.semantic_memory),
            'procedural_memory_count': len(self.procedural_memory),
            'knowledge_graph_nodes': self.knowledge_graph.number_of_nodes() if self.knowledge_graph else 0,
            'knowledge_graph_edges': self.knowledge_graph.number_of_edges() if self.knowledge_graph else 0,
            'vector_db_enabled': self.use_vector_db
        }
    
    async def _move_to_long_term(self, memory: Memory):
        """Move memory from working to long-term storage"""
        if memory.memory_type == "episodic" or memory.memory_type == "working":
            self.episodic_memory.append(memory)
    
    async def _save_memories(self):
        """Save memories to disk"""
        try:
            # Save episodic memories
            episodic_file = self.data_dir / "episodic_memory.json"
            with open(episodic_file, 'w') as f:
                json.dump(
                    [m.to_dict() for m in self.episodic_memory[-1000:]],  # Keep last 1000
                    f, indent=2
                )
            
            # Save semantic memories
            semantic_file = self.data_dir / "semantic_memory.json"
            with open(semantic_file, 'w') as f:
                json.dump(self.semantic_memory, f, indent=2)
            
            # Save procedural memories
            procedural_file = self.data_dir / "procedural_memory.json"
            with open(procedural_file, 'w') as f:
                json.dump(self.procedural_memory, f, indent=2)
                
        except Exception as e:
            print(f"   Save error: {e}")
    
    async def _load_memories(self):
        """Load memories from disk"""
        try:
            # Load episodic
            episodic_file = self.data_dir / "episodic_memory.json"
            if episodic_file.exists():
                with open(episodic_file, 'r') as f:
                    data = json.load(f)
                    for item in data:
                        self.episodic_memory.append(Memory(
                            content=item['content'],
                            timestamp=datetime.fromisoformat(item['timestamp']),
                            memory_type=item['memory_type'],
                            importance=item['importance'],
                            metadata=item.get('metadata', {})
                        ))
            
            # Load semantic
            semantic_file = self.data_dir / "semantic_memory.json"
            if semantic_file.exists():
                with open(semantic_file, 'r') as f:
                    self.semantic_memory = json.load(f)
            
            # Load procedural
            procedural_file = self.data_dir / "procedural_memory.json"
            if procedural_file.exists():
                with open(procedural_file, 'r') as f:
                    self.procedural_memory = json.load(f)
                    
        except Exception as e:
            print(f"   Load error: {e}")


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

async def example_usage():
    """Example of how to use the Advanced Memory System"""
    
    # Initialize
    memory = AdvancedMemorySystem()
    await memory.initialize()
    
    # Store different types of memories
    await memory.store(
        "User asked about Python programming at 3 PM",
        memory_type="episodic",
        importance=0.6,
        metadata={'topic': 'programming', 'language': 'python'}
    )
    
    await memory.store(
        "User prefers Python over JavaScript for backend development",
        memory_type="semantic",
        importance=0.8
    )
    
    await memory.store(
        "To create a Flask app: 1) Install Flask, 2) Create app.py, 3) Run with flask run",
        memory_type="procedural",
        importance=0.7,
        metadata={'task': 'create_flask_app'}
    )
    
    # Add to knowledge graph
    await memory.add_to_knowledge_graph("User", "prefers", "Python")
    await memory.add_to_knowledge_graph("Python", "used_for", "Backend Development")
    await memory.add_to_knowledge_graph("User", "works_on", "JARVIS Project")
    
    # Retrieve memories
    results = await memory.retrieve("Python programming")
    print("\n🔍 Search Results for 'Python programming':")
    for result in results:
        print(f"   • {result['content']}")
    
    # Query knowledge graph
    graph_data = await memory.query_knowledge_graph("User")
    print(f"\n📊 Knowledge Graph for 'User':")
    for rel in graph_data.get('relationships', []):
        print(f"   • User -{rel['relationship']}-> {rel['entity']}")
    
    # Get stats
    stats = memory.get_memory_stats()
    print(f"\n📈 Memory Statistics:")
    for key, value in stats.items():
        print(f"   • {key}: {value}")


if __name__ == "__main__":
    asyncio.run(example_usage())
