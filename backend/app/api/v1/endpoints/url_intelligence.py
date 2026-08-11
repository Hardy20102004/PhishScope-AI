from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import AnyHttpUrl, BaseModel, field_validator

from app.services.gemini_service import gemini_service
from app.url_intelligence.orchestrator import InvestigationOrchestrator

router = APIRouter()


class URLSubmission(BaseModel):
    """
    Input model for URL investigation.
    
    Fixed BUG-004: Added proper URL validation using Pydantic's AnyHttpUrl
    internally, with a user-friendly error message. Also added max length limit.
    """
    url: str
    
    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("URL cannot be empty")
        
        v = v.strip()
        
        # Length guard — prevents abuse
        if len(v) > 2048:
            raise ValueError("URL exceeds maximum allowed length of 2048 characters")
        
        # Must start with http:// or https://
        if not v.startswith(("http://", "https://")):
            raise ValueError(
                "URL must include a scheme. Use 'https://example.com' format. "
                "This tool only supports HTTP/HTTPS URLs."
            )
        
        return v


class QuickClassifyRequest(BaseModel):
    url: str


class URLInvestigationResponse(BaseModel):
    canonical_url: str
    parsed: Dict[str, Any]
    intelligence: Dict[str, Any]
    redirect_chain: list
    infrastructure: Dict[str, Any]
    brand: Dict[str, Any]
    risk_score: Dict[str, Any]
    ai_summary: Dict[str, Any]


@router.post(
    "/investigate",
    response_model=URLInvestigationResponse,
    status_code=status.HTTP_200_OK,
    summary="Deep URL Investigation",
    description=(
        "Submits a URL for full phishing intelligence investigation powered by Google Gemini AI. "
        "Returns parsed URL structure, DNS/TLS infrastructure, redirect chain analysis, "
        "brand impersonation detection, risk scoring, and AI-generated threat narrative."
    ),
)
async def investigate_url(submission: URLSubmission):
    """
    Full URL investigation endpoint.
    Powered by Gemini AI for threat narrative generation.
    """
    try:
        results = await InvestigationOrchestrator.run_investigation(submission.url)
        return results
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid URL: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Investigation failed: {str(e)}"
        )


@router.post(
    "/quick-classify",
    summary="Quick Phishing Classification",
    description=(
        "Fast URL classification using Gemini Flash model. "
        "Returns a PHISHING/SUSPICIOUS/SAFE verdict in seconds. "
        "Use /investigate for full deep analysis."
    ),
    status_code=status.HTTP_200_OK,
)
async def quick_classify_url(request: QuickClassifyRequest):
    """
    Quick classification using Gemini 2.5 Flash — fast, low-latency verdict.
    """
    if not request.url.strip():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="URL cannot be empty")
    
    try:
        result = await gemini_service.quick_classify(request.url)
        return {
            "url": request.url,
            "classification": result,
            "gemini_available": gemini_service.is_available,
            "model": gemini_service.active_model,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Classification failed: {str(e)}"
        )


@router.get(
    "/ai-status",
    summary="Gemini AI Service Status",
    description="Returns the current status of the Gemini AI integration and active model.",
    status_code=status.HTTP_200_OK,
)
async def get_ai_status():
    """Returns Gemini AI service health and active model info."""
    from app.core.config import settings
    return {
        "gemini_configured": gemini_service.is_available,
        "active_model": gemini_service.active_model,
        "primary_model": settings.GEMINI_PRIMARY_MODEL,
        "fast_model": settings.GEMINI_FAST_MODEL,
        "fallback_models": settings.gemini_fallback_model_list,
        "all_supported_models": [
            "gemini-2.5-pro",
            "gemini-2.5-flash",
            "gemini-2.0-flash",
            "gemini-1.5-pro",
            "gemini-1.5-flash",
        ],
        "status": "operational" if gemini_service.is_available else "degraded (using rule-based fallback)",
    }
