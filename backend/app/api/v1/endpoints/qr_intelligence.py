from typing import Any, Dict, Optional
import io

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from pydantic import BaseModel
from PIL import Image
import cv2
import numpy as np

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

class QRScanResponse(BaseModel):
    success: bool
    raw_payload: Optional[str] = None
    payload_type: Optional[str] = None
    message: str
    metadata: Dict[str, Any]

@router.post("/investigate", response_model=QRInvestigationResponse, status_code=status.HTTP_200_OK)
async def investigate_qr(submission: QRSubmission):
    """
    Submits a mock QR payload for deep intelligence investigation.
    """
    try:
        results = await QRInvestigationOrchestrator.run_investigation(submission.raw_payload)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to investigate QR code: {str(e)}"
        )

@router.post("/scan-image", response_model=QRScanResponse, status_code=status.HTTP_200_OK)
async def scan_qr_image(file: UploadFile = File(...)):
    """
    Upload a QR image file (PNG, JPG, WEBP, etc.) to scan and extract the embedded QR payload data.
    """
    try:
        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="Empty image file uploaded")

        # Extract metadata using PIL
        pil_img = Image.open(io.BytesIO(contents))
        width, height = pil_img.size
        img_format = pil_img.format or "JPEG"

        # Convert to OpenCV matrix for QR detection
        nparr = np.frombuffer(contents, np.uint8)
        cv_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        decoded_text = ""
        if cv_img is not None:
            detector = cv2.QRCodeDetector()
            decoded_text, _, _ = detector.detectAndDecode(cv_img)
            
            # Grayscale fallback
            if not decoded_text:
                gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
                decoded_text, _, _ = detector.detectAndDecode(gray)

        payload_type = "text"
        if decoded_text.startswith("http://") or decoded_text.startswith("https://"):
            payload_type = "url"
        elif decoded_text.startswith("upi://pay"):
            payload_type = "payment_upi"
        elif decoded_text.startswith("WIFI:"):
            payload_type = "wifi"
        elif decoded_text.startswith("MECARD:") or decoded_text.startswith("BEGIN:VCARD"):
            payload_type = "contact"

        metadata = {
            "filename": file.filename,
            "resolution": f"{width}x{height}",
            "file_size_bytes": len(contents),
            "format": img_format.lower(),
            "contains_multiple_qrs": False
        }

        if decoded_text:
            return QRScanResponse(
                success=True,
                raw_payload=decoded_text,
                payload_type=payload_type,
                message=f"Successfully extracted QR data ({payload_type})",
                metadata=metadata
            )
        else:
            return QRScanResponse(
                success=False,
                raw_payload=None,
                payload_type=None,
                message="No QR code could be detected in the uploaded image. Please try a clearer photo or enter payload manually.",
                metadata=metadata
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to scan QR image: {str(e)}"
        )

