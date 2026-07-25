import json
from typing import Any, Dict, List

import structlog
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from app.ai_brain.orchestrator import ai_brain_orchestrator
from app.schemas.ai_brain import OrchestrationRequest, OrchestrationResponse

router = APIRouter()
logger = structlog.get_logger("phoenix.api.ai_brain")

# In a real enterprise setting, these endpoints would be protected by robust OAuth2 dependencies
# e.g., @router.post("/orchestrate", response_model=OrchestrationResponse, dependencies=[Depends(get_current_active_user)])

@router.post("/orchestrate", response_model=OrchestrationResponse, summary="Execute Enterprise AI Security Orchestration")
async def execute_orchestration(request: OrchestrationRequest) -> Any:
    """
    Submits a complex security investigation query to the AI Security Brain.
    Automatically handles intent resolution, evidence aggregation, multi-provider failover,
    prompt caching, and rigorous response validation (OWASP Top 10 LLM / NIST AI RMF).
    """
    try:
        result = await ai_brain_orchestrator.orchestrate(
            input_text=request.input_text,
            capability=request.capability,
            case_id=str(request.case_id) if request.case_id else None,
            investigation_id=str(request.investigation_id) if request.investigation_id else None,
            session_id=request.session_id,
            tenant_id=str(request.tenant_id) if request.tenant_id else None,
            user_id=str(request.user_id) if request.user_id else None,
            additional_context=request.additional_context,
            override_model_id=request.override_model_id
        )
        return OrchestrationResponse(**result)
    except Exception as e:
        logger.error("orchestration_endpoint_failure", error=str(e))
        raise HTTPException(status_code=500, detail=f"AI Orchestration Engine Error: {str(e)}")

@router.post("/stream", summary="Stream Real-Time AI Inference")
async def execute_streaming(request: OrchestrationRequest) -> StreamingResponse:
    """
    Asynchronous Server-Sent Events (SSE) compatible streaming endpoint for conversational UI generation.
    """
    async def event_generator():
        try:
            async for chunk_data in ai_brain_orchestrator.stream_orchestrate(
                input_text=request.input_text,
                capability=request.capability,
                session_id=request.session_id,
                tenant_id=str(request.tenant_id) if request.tenant_id else None,
                override_model_id=request.override_model_id
            ):
                # Format as SSE (Server-Sent Event) payload
                yield f"data: {json.dumps(chunk_data)}\n\n"
        except Exception as e:
            logger.error("streaming_endpoint_failure", error=str(e))
            yield f"data: {json.dumps({'event': 'error', 'message': str(e)})}\n\n"
            
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.get("/health-analytics", summary="Get AI Brain Telemetry and Cost Analytics")
async def get_health_and_analytics(tenant_id: str = None) -> Any:
    """
    Retrieves global provider circuit-breaker status, latency metrics, token consumption, and cost estimates.
    """
    return await ai_brain_orchestrator.get_system_health_and_analytics(tenant_id)

@router.get("/providers", response_model=List[Dict[str, Any]], summary="List AI Providers")
async def get_providers() -> Any:
    """Returns active LLM providers and their current failover circuit-breaker statuses."""
    return ai_brain_orchestrator.providers.list_providers()

@router.get("/models", summary="List Available AI Models")
async def get_models() -> Any:
    """Returns all registered enterprise models, context limits, and per-token cost schemas."""
    return ai_brain_orchestrator.models.list_all()

@router.get("/capabilities", summary="List SOC Investigation Capabilities")
async def get_capabilities() -> Any:
    """Returns AI capability mappings with default and fallback execution targets."""
    return ai_brain_orchestrator.capabilities.list_capabilities()

@router.get("/prompts", summary="List Template Registry")
async def get_prompts() -> Any:
    """Returns system prompt registry used for standardized case summaries and threat intel reports."""
    return ai_brain_orchestrator.prompts.list_templates()

@router.delete("/memory/{session_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Clear Conversation Memory")
async def clear_session_memory(session_id: str):
    """Purges interactive session memory history."""
    ai_brain_orchestrator.conversations.memory.store_memory(
        tier=ai_brain_orchestrator.conversations.memory._get_tier_store(None), # Bypass check for deletion
        key=session_id,
        data={},
        ttl_seconds=-1 # Force expiry
    )
    # Actually just delete it directly from memory
    store = ai_brain_orchestrator.conversations.memory._get_tier_store(MemoryTier.CONVERSATION)
    if session_id in store:
        del store[session_id]
    return None
