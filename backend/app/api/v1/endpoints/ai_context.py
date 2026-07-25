from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.ai_context.builder import ContextManager
from app.api import deps
from app.models.ai_context import ContextAuditLog, ContextPolicy
from app.schemas.ai_context import ContextPolicyResponse, ContextRequest, ContextResponse

router = APIRouter()

def get_context_manager(db: Session = Depends(deps.get_db)) -> ContextManager:
    return ContextManager(db)

@router.post("/build", response_model=ContextResponse)
async def build_context(
    request: ContextRequest,
    manager: ContextManager = Depends(get_context_manager)
):
    """
    Builds, validates, and compresses AI Context dynamically based on the investigation state or query.
    """
    return manager.build_context(request)

@router.get("/policies", response_model=List[ContextPolicyResponse])
async def list_policies(db: Session = Depends(deps.get_db)):
    """
    List active context policies (e.g., PII Redaction, Token Limits).
    """
    policies = db.query(ContextPolicy).all()
    return [ContextPolicyResponse.from_orm(p) for p in policies]

@router.get("/analytics")
async def get_analytics(db: Session = Depends(deps.get_db)):
    """
    Retrieve token usage, latency, and compression metrics.
    """
    logs = db.query(ContextAuditLog).all()
    
    total_original = sum(log.original_tokens or 0 for log in logs)
    total_compressed = sum(log.compressed_tokens or 0 for log in logs)
    
    avg_latency = 0.0
    if logs:
        latencies = [log.build_latency_ms for log in logs if log.build_latency_ms]
        if latencies:
            avg_latency = sum(latencies) / len(latencies)
            
    saved_tokens = total_original - total_compressed
    
    return {
        "total_builds": len(logs),
        "total_original_tokens": total_original,
        "total_compressed_tokens": total_compressed,
        "tokens_saved": saved_tokens,
        "average_build_latency_ms": round(avg_latency, 2)
    }
