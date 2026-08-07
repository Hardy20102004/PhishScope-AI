import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.attack_path import AssetNode, AssetRelationship

class BlastRadiusEngine:
    """
    Calculates the downstream impact by traversing outward from a compromised node.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def calculate_blast_radius(self, tenant_id: uuid.UUID, compromised_node_id: uuid.UUID) -> list[str]:
        """
        MVP: Simulates outward traversal. Finds all downstream assets reachable from the compromised node.
        """
        res = await self.db.execute(
            select(AssetRelationship).where(AssetRelationship.source_node_id == compromised_node_id)
        )
        edges = res.scalars().all()
        
        impacted_nodes = []
        for edge in edges:
            node_res = await self.db.execute(select(AssetNode).where(AssetNode.id == edge.target_node_id))
            tgt = node_res.scalar_one()
            impacted_nodes.append(f"{tgt.node_type}:{tgt.name}")
            
        return impacted_nodes
