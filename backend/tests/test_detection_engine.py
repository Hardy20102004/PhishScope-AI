import pytest
import uuid
from httpx import AsyncClient

from app.models.detection import DetectionRule
from app.detection_engine.validation import RuleValidationEngine
from app.detection_engine.workflow import RuleApprovalWorkflow

pytestmark = pytest.mark.asyncio

async def test_sigma_validation_success():
    valid_sigma = """
title: Suspicious Execution
logsource:
    category: process_creation
    product: windows
detection:
    selection:
        CommandLine|contains: 'mimikatz'
    condition: selection
    """
    result = RuleValidationEngine.validate_payload("SIGMA", valid_sigma)
    assert result["is_valid"] is True
    assert len(result["errors"]) == 0

async def test_sigma_validation_failure():
    invalid_sigma = """
title: Suspicious Execution
# missing logsource and detection blocks
    """
    result = RuleValidationEngine.validate_payload("SIGMA", invalid_sigma)
    assert result["is_valid"] is False
    assert "missing required sections" in result["errors"][0]

async def test_yara_validation_success():
    valid_yara = """
rule maldoc {
    strings:
        $a = "AutoOpen"
    condition:
        $a
}
    """
    result = RuleValidationEngine.validate_payload("YARA", valid_yara)
    assert result["is_valid"] is True

async def test_yara_validation_failure():
    invalid_yara = """
maldoc {
    strings:
        $a = "AutoOpen"
}
    """
    result = RuleValidationEngine.validate_payload("YARA", invalid_yara)
    assert result["is_valid"] is False
    assert "Invalid YARA syntax" in result["errors"][0]

async def test_workflow_invalid_transition(db_session):
    workflow = RuleApprovalWorkflow(db_session)
    # Testing mock transition without creating actual DB object, just asserting the logic
    # The workflow relies on DB, so we test the constant map instead for this unit test
    
    assert "APPROVED" not in workflow.VALID_TRANSITIONS["DEPLOYED"]
    assert "DEPLOYED" in workflow.VALID_TRANSITIONS["READY_FOR_DEPLOYMENT"]
