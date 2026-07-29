import uuid
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api import deps
from app.models.user import User
from app.models.detection import DetectionRule, DetectionRuleVersion, RuleApprovalRecord
from app.schemas.detection import (
    DetectionRuleCreate, DetectionRuleUpdate, DetectionRuleResponse,
    RuleApprovalRecordCreate, RuleApprovalRecordResponse,
    DetectionRuleVersionResponse, RuleTestResultResponse
)

from app.detection_engine.validation import RuleValidationEngine
from app.detection_engine.versioning import RuleVersionManager
from app.detection_engine.workflow import RuleApprovalWorkflow
from app.detection_engine.testing import RuleTestingEngine
from app.detection_engine.authoring import RuleAuthoringEngine

router = APIRouter()

@router.post("/", response_model=DetectionRuleResponse, status_code=status.HTTP_201_CREATED)
async def create_detection_rule(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    rule_in: DetectionRuleCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new detection rule (Draft).
    """
    # 1. Validate syntax
    val_result = RuleValidationEngine.validate_payload(rule_in.rule_type, rule_in.payload)
    if not val_result["is_valid"]:
        raise HTTPException(status_code=400, detail=f"Validation failed: {val_result['errors']}")

    # 2. Create Rule
    rule = DetectionRule(
        tenant_id=current_user.tenant_id,
        name=rule_in.name,
        description=rule_in.description,
        rule_type=rule_in.rule_type,
        severity=rule_in.severity,
        mitre_tactics=rule_in.mitre_tactics,
        mitre_techniques=rule_in.mitre_techniques,
        tags=rule_in.tags,
        author_id=current_user.id,
        owner_id=current_user.id,
        status="DRAFT"
    )
    db.add(rule)
    await db.flush()

    # 3. Create Version 1
    version_manager = RuleVersionManager(db)
    await version_manager.create_new_version(
        rule=rule,
        new_payload=rule_in.payload,
        author_id=current_user.id,
        change_summary="Initial commit"
    )
    
    return rule

@router.get("/", response_model=List[DetectionRuleResponse])
async def list_detection_rules(
    db: AsyncSession = Depends(deps.get_async_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    List all detection rules for tenant.
    """
    result = await db.execute(
        select(DetectionRule)
        .where(DetectionRule.tenant_id == current_user.tenant_id)
        .order_by(DetectionRule.updated_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

@router.patch("/{rule_id}/status", response_model=DetectionRuleResponse)
async def transition_rule_status(
    rule_id: uuid.UUID,
    approval_in: RuleApprovalRecordCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Transitions the rule through the approval lifecycle (e.g., DRAFT -> IN_REVIEW -> APPROVED).
    """
    workflow = RuleApprovalWorkflow(db)
    try:
        rule = await workflow.transition_status(
            rule_id=rule_id,
            new_status=approval_in.status_changed_to,
            user_id=current_user.id,
            notes=approval_in.notes
        )
        return rule
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{rule_id}/test", response_model=RuleTestResultResponse)
async def run_rule_test(
    rule_id: uuid.UUID,
    dataset_name: str,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Executes a test run of the rule against a specified dataset.
    """
    # Fetch rule to get current version
    result = await db.execute(select(DetectionRule).where(DetectionRule.id == rule_id))
    rule = result.scalar_one_or_none()
    if not rule:
         raise HTTPException(status_code=404, detail="Rule not found")
         
    # Fetch latest version id
    ver_result = await db.execute(
        select(DetectionRuleVersion).where(
            DetectionRuleVersion.rule_id == rule.id,
            DetectionRuleVersion.version == rule.current_version
        )
    )
    version = ver_result.scalar_one_or_none()
    if not version:
         raise HTTPException(status_code=404, detail="Version not found")

    tester = RuleTestingEngine(db)
    test_result = await tester.execute_test(rule.id, version.id, dataset_name)
    return test_result

@router.post("/ai/suggest")
async def generate_ai_suggestions(
    payload: dict,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Generate AI suggestions and MITRE mappings based on a draft rule payload.
    """
    author = RuleAuthoringEngine(db)
    raw_payload = payload.get("payload", "")
    return await author.generate_ai_suggestions(raw_payload)
