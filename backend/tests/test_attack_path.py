import pytest
import uuid
from app.attack_path.graph_engine import GraphEngine
from app.attack_path.exposure_engine import ExposureEngine
from app.attack_path.blast_radius_engine import BlastRadiusEngine

pytestmark = pytest.mark.asyncio

async def test_attack_path_simulation(db_session):
    tenant_id = uuid.uuid4()
    
    ge = GraphEngine(db_session)
    
    # 1. Create Nodes
    user = await ge.add_node(tenant_id, "USER", "Phished_Dev", False)
    server = await ge.add_node(tenant_id, "SERVER", "JUMP_HOST_01", False)
    db = await ge.add_node(tenant_id, "DATABASE", "PROD_DB", True)
    
    # 2. Create Relationships
    await ge.add_relationship(tenant_id, user.id, server.id, "HAS_SESSION")
    await ge.add_relationship(tenant_id, server.id, db.id, "CAN_ASSUME_ROLE")
    
    # 3. Simulate Pathfinding
    ee = ExposureEngine(db_session)
    path = await ee.simulate_attack_path(tenant_id, user.id, db.id)
    
    assert path.start_node_id == user.id
    assert path.target_node_id == db.id
    assert path.path_complexity == 3 # 3 nodes in sequence
    
    # 4. Test Blast Radius (from Server)
    bre = BlastRadiusEngine(db_session)
    impact = await bre.calculate_blast_radius(tenant_id, server.id)
    
    assert len(impact) == 1
    assert "DATABASE:PROD_DB" in impact[0]
