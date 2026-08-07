import asyncio
from app.db.session import SessionLocal
from app.services.knowledge_evolution.manager import KnowledgeEvolutionManager

db = SessionLocal()
manager = KnowledgeEvolutionManager(db)

try:
    print("Nodes:", manager.ontology.get_nodes())
    print("Recommendations:", manager.schema.get_pending_recommendations())
    print("Relationships:", manager.discovery.discover_relationships())
    print("Overview:", manager.get_overview_stats())
except Exception as e:
    print(f"Error: {e}")
