import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.attack_path import AssetNode, AssetRelationship

class GraphEngine:
    """
    Manages the CRUD operations for Asset Nodes and their Relationships.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_node(self, tenant_id: uuid.UUID, node_type: str, name: str, is_critical: bool, properties: dict = None) -> AssetNode:
        node = AssetNode(
            tenant_id=tenant_id,
            node_type=node_type,
            name=name,
            is_critical=is_critical,
            properties=properties or {}
        )
        self.db.add(node)
        await self.db.commit()
        await self.db.refresh(node)
        return node

    async def add_relationship(self, tenant_id: uuid.UUID, source_id: uuid.UUID, target_id: uuid.UUID, rel_type: str) -> AssetRelationship:
        rel = AssetRelationship(
            tenant_id=tenant_id,
            source_node_id=source_id,
            target_node_id=target_id,
            relationship_type=rel_type
        )
        self.db.add(rel)
        await self.db.commit()
        await self.db.refresh(rel)
        return rel
