from datetime import datetime, timezone
import uuid
from typing import Any, Optional
import structlog
from app.schemas.base import APIResponse, APIErrorResponse, ResponseMeta, ErrorPayload, ErrorDetail

def generate_meta() -> ResponseMeta:
    """Helper to generate standard metadata for responses."""
    # Attempt to grab the request_id from structlog context if available
    context = structlog.contextvars.get_contextvars()
    request_id = context.get("request_id", str(uuid.uuid4()))
    
    return ResponseMeta(
        request_id=request_id,
        timestamp=datetime.now(timezone.utc).isoformat() + "Z",
        version="v1.0"
    )

def success_response(data: Any, pagination: Optional[Any] = None) -> APIResponse:
    """Helper to wrap data into the standard APIResponse format."""
    meta = generate_meta()
    if pagination:
        meta.pagination = pagination
    return APIResponse(status="success", data=data, meta=meta)

def error_response(code: str, message: str, details: Optional[list] = None) -> APIErrorResponse:
    """Helper to wrap errors into the standard APIErrorResponse format."""
    payload = ErrorPayload(code=code, message=message, details=details)
    return APIErrorResponse(status="error", error=payload, meta=generate_meta())
