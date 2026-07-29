import pytest
import uuid

from app.models.incident_response import DFIRCase, Incident
from app.incident_response.evidence_manager import EvidenceManager
from app.incident_response.incident_manager import IncidentManager

pytestmark = pytest.mark.asyncio

async def test_incident_creation_provisions_case(db_session):
    tenant_id = uuid.uuid4()
    user_id = uuid.uuid4()
    manager = IncidentManager(db_session)
    
    incident = await manager.create_incident(
        title="Test Incident",
        description="A test",
        severity="HIGH",
        tenant_id=tenant_id,
        user_id=user_id
    )
    
    assert incident.id is not None
    assert incident.status == "NEW"
    
    # Assert a default DFIR Case was created and linked
    assert len(incident.cases) == 1
    assert incident.cases[0].case_type == "FORENSICS"

async def test_evidence_chain_of_custody(db_session):
    incident = Incident(title="Mock Incident", tenant_id=uuid.uuid4())
    db_session.add(incident)
    await db_session.flush()
    # Setup mock case
    case = DFIRCase(title="Mock Case", case_type="FORENSICS", incident_id=incident.id)
    db_session.add(case)
    await db_session.commit()
    await db_session.refresh(case)
    
    manager = EvidenceManager(db_session)
    user_id = uuid.uuid4()
    
    # Attach evidence
    evidence = await manager.attach_evidence(
        case_id=case.id,
        artifact_type="FILE_HASH",
        artifact_value="some_hash_value",
        source="EDR",
        user_id=user_id
    )
    
    # Assert Evidence stored
    assert evidence.artifact_value == "some_hash_value"
    
    # Assert Chain of Custody generated
    assert len(evidence.chain_of_custody) == 1
    coc_log = evidence.chain_of_custody[0]
    
    assert coc_log.action == "COLLECTED"
    assert coc_log.digital_signature is not None
    
    # Test Transfer
    transfer_log = await manager.transfer_evidence(
        evidence_id=evidence.id,
        user_id=user_id,
        notes="Sent to sandbox"
    )
    
    assert transfer_log.action == "TRANSFERRED"
    # Ensure signature matches original collection hash
    assert transfer_log.digital_signature == coc_log.digital_signature
