from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any

from app.qr_intelligence.orchestrator import QRInvestigationOrchestrator

router = APIRouter()

class QRSubmission(BaseModel):
    raw_payload: str

class QRInvestigationResponse(BaseModel):
    image_metadata: Dict[str, Any]
    decoded_payload: Dict[str, Any]
    visual_analysis: Dict[str, Any]
    tampering_analysis: Dict[str, Any]
    payment_analysis: Dict[str, Any]
    risk_score: Dict[str, Any]
    ai_summary: Dict[str, str]

@router.post("/investigate", response_model=QRInvestigationResponse, status_code=status.HTTP_200_OK)
async def investigate_qr(submission: QRSubmission):
    """
    Submits a mock QR payload for deep intelligence investigation.
    In a full implementation, this would accept a multipart/form-data image upload.
    """
    try:
        results = await QRInvestigationOrchestrator.run_investigation(submission.raw_payload)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to investigate QR code: {str(e)}"
        )
