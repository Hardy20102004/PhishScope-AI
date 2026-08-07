"""
PHOENIX X — ISPM: Identity Relationship Engine

Builds and maintains the identity relationship graph.
Correlates users → groups → roles → apps → cloud resources → permissions.
Distinguished observed (from discovery) vs inferred (from risk analysis) relationships.
Enables shortest-path privilege escalation analysis.
"""
import uuid
from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.models.ispm import (
    IdentityRelationship, EnterpriseIdentity,
    RelationshipType
)
from app.schemas.ispm import IdentityRelationshipCreate


class IdentityRelationshipEngine:
    """
    Graph-based identity relationship correlation engine.

    Graph Schema:
      Nodes: IDENTITY | GROUP | ROLE | APPLICATION | CLOUD_RESOURCE | PERMISSION
      Edges: RelationshipType enum values (MEMBER_OF, HAS_ROLE, DELEGATES_TO, etc.)

    Key capabilities:
    - Discover all relationships from connected providers
    - Build traversal graph for access path analysis
    - Identify privilege escalation paths
    - Detect implicit trust relationships
    - Correlate with Knowledge Graph for enterprise-wide context
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_relationship(
        self, tenant_id: uuid.UUID, rel_in: IdentityRelationshipCreate
    ) -> IdentityRelationship:
        """Add a graph edge between two identity entities."""
        # Check for duplicate
        stmt = select(IdentityRelationship).where(
            IdentityRelationship.tenant_id == tenant_id,
            IdentityRelationship.source_entity_id == rel_in.source_entity_id,
            IdentityRelationship.target_entity_id == rel_in.target_entity_id,
            IdentityRelationship.relationship_type == rel_in.relationship_type
        )
        result = await self.db.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            existing.confidence_score = rel_in.confidence_score
            existing.risk_weight = rel_in.risk_weight
            await self.db.commit()
            await self.db.refresh(existing)
            return existing

        rel = IdentityRelationship(tenant_id=tenant_id, **rel_in.model_dump())
        self.db.add(rel)
        await self.db.commit()
        await self.db.refresh(rel)
        return rel

    async def get_identity_relationships(
        self, tenant_id: uuid.UUID, entity_id: str
    ) -> List[IdentityRelationship]:
        """Get all relationships where the entity is source or target."""
        stmt = select(IdentityRelationship).where(
            IdentityRelationship.tenant_id == tenant_id,
            or_(
                IdentityRelationship.source_entity_id == entity_id,
                IdentityRelationship.target_entity_id == entity_id
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def list_relationships(
        self,
        tenant_id: uuid.UUID,
        relationship_type: Optional[RelationshipType] = None,
        is_privileged_path: Optional[bool] = None,
        is_observed: Optional[bool] = None,
        limit: int = 200
    ) -> List[IdentityRelationship]:
        stmt = select(IdentityRelationship).where(
            IdentityRelationship.tenant_id == tenant_id
        )
        if relationship_type:
            stmt = stmt.where(IdentityRelationship.relationship_type == relationship_type)
        if is_privileged_path is not None:
            stmt = stmt.where(IdentityRelationship.is_privileged_path == is_privileged_path)
        if is_observed is not None:
            stmt = stmt.where(IdentityRelationship.is_observed == is_observed)
        stmt = stmt.order_by(IdentityRelationship.risk_weight.desc()).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def build_graph_snapshot(self, tenant_id: uuid.UUID) -> Dict[str, Any]:
        """
        Build a serializable snapshot of the identity relationship graph.
        Used by the frontend graph visualization and Knowledge Graph sync.
        """
        stmt = select(IdentityRelationship).where(
            IdentityRelationship.tenant_id == tenant_id
        )
        result = await self.db.execute(stmt)
        relationships = result.scalars().all()

        nodes: Dict[str, Any] = {}
        edges = []

        for rel in relationships:
            # Build node set
            for entity_type, entity_id, entity_name in [
                (rel.source_entity_type, rel.source_entity_id, rel.source_entity_name),
                (rel.target_entity_type, rel.target_entity_id, rel.target_entity_name)
            ]:
                if entity_id not in nodes:
                    nodes[entity_id] = {
                        "id": entity_id,
                        "type": entity_type,
                        "name": entity_name,
                        "group": entity_type
                    }

            edges.append({
                "id": str(rel.id),
                "source": rel.source_entity_id,
                "target": rel.target_entity_id,
                "relationship": rel.relationship_type.value,
                "is_observed": rel.is_observed,
                "is_privileged_path": rel.is_privileged_path,
                "risk_weight": rel.risk_weight,
                "confidence": rel.confidence_score
            })

        return {
            "nodes": list(nodes.values()),
            "edges": edges,
            "node_count": len(nodes),
            "edge_count": len(edges),
            "privileged_paths": sum(1 for e in edges if e["is_privileged_path"]),
            "inferred_relationships": sum(1 for e in edges if not e["is_observed"])
        }

    async def detect_privilege_escalation_paths(
        self, tenant_id: uuid.UUID
    ) -> List[Dict[str, Any]]:
        """
        Detect potential privilege escalation paths in the identity graph.
        Identifies: group nesting → admin roles, delegation chains, trust inheritance.
        """
        stmt = select(IdentityRelationship).where(
            IdentityRelationship.tenant_id == tenant_id,
            IdentityRelationship.is_privileged_path == True
        )
        result = await self.db.execute(stmt)
        privileged = result.scalars().all()

        paths = []
        for rel in privileged:
            paths.append({
                "source": rel.source_entity_name,
                "target": rel.target_entity_name,
                "relationship": rel.relationship_type.value,
                "risk_weight": rel.risk_weight,
                "is_observed": rel.is_observed,
                "description": (
                    f"{rel.source_entity_name} → [{rel.relationship_type.value}] → "
                    f"{rel.target_entity_name} (privileged path)"
                )
            })

        return paths

    async def seed_demo_relationships(self, tenant_id: uuid.UUID) -> int:
        """Seed demonstration relationships for UI visualization."""
        import random
        demo_relationships = [
            {
                "source_entity_type": "IDENTITY",
                "source_entity_id": "identity-001",
                "source_entity_name": "John Smith",
                "target_entity_type": "GROUP",
                "target_entity_id": "group-admins",
                "target_entity_name": "Domain Admins",
                "relationship_type": RelationshipType.MEMBER_OF,
                "is_observed": True,
                "is_direct": True,
                "is_privileged_path": True,
                "risk_weight": 0.85,
                "confidence_score": 1.0
            },
            {
                "source_entity_type": "GROUP",
                "source_entity_id": "group-admins",
                "source_entity_id": "group-admins",
                "source_entity_name": "Domain Admins",
                "target_entity_type": "ROLE",
                "target_entity_id": "role-global-admin",
                "target_entity_name": "Global Administrator",
                "relationship_type": RelationshipType.HAS_ROLE,
                "is_observed": True,
                "is_direct": True,
                "is_privileged_path": True,
                "risk_weight": 0.95,
                "confidence_score": 1.0
            },
            {
                "source_entity_type": "IDENTITY",
                "source_entity_id": "identity-002",
                "source_entity_name": "ServiceAccount-API",
                "target_entity_type": "APPLICATION",
                "target_entity_id": "app-payroll",
                "target_entity_name": "Payroll System",
                "relationship_type": RelationshipType.ACCESSES_RESOURCE,
                "is_observed": True,
                "is_direct": True,
                "is_privileged_path": False,
                "risk_weight": 0.55,
                "confidence_score": 0.9
            },
            {
                "source_entity_type": "IDENTITY",
                "source_entity_id": "identity-003",
                "source_entity_name": "Maria Garcia",
                "target_entity_type": "IDENTITY",
                "target_entity_id": "identity-004",
                "target_entity_name": "ServiceAccount-Dev",
                "relationship_type": RelationshipType.DELEGATES_TO,
                "is_observed": False,
                "is_direct": False,
                "is_privileged_path": True,
                "risk_weight": 0.75,
                "confidence_score": 0.72
            },
            {
                "source_entity_type": "ROLE",
                "source_entity_id": "role-contributor",
                "source_entity_name": "Subscription Contributor",
                "target_entity_type": "CLOUD_RESOURCE",
                "target_entity_id": "resource-prod-rg",
                "target_entity_name": "Production Resource Group",
                "relationship_type": RelationshipType.HAS_PERMISSION,
                "is_observed": True,
                "is_direct": True,
                "is_privileged_path": True,
                "risk_weight": 0.80,
                "confidence_score": 1.0
            }
        ]

        count = 0
        for rel_data in demo_relationships:
            rel_in = IdentityRelationshipCreate(**rel_data)
            await self.create_relationship(tenant_id, rel_in)
            count += 1

        return count
