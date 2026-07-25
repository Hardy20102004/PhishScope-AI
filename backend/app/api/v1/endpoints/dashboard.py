from fastapi import APIRouter, Depends
from typing import Any
from app.api.deps import get_current_user
from app.schemas.base import APIResponse
from app.api.responses import success_response
from app.models.user import User

router = APIRouter()

@router.get("/stats", response_model=APIResponse[Any])
def get_dashboard_stats(current_user: User = Depends(get_current_user)) -> Any:
    """Mock endpoint to provide data for the Risk Distribution Chart."""
    # In Phase 10, this will calculate real stats from the DB
    return success_response([
        {"name": "High Risk", "value": 45, "color": "#ef4444"},
        {"name": "Medium Risk", "value": 30, "color": "#f59e0b"},
        {"name": "Low Risk", "value": 15, "color": "#eab308"},
        {"name": "Clean", "value": 10, "color": "#22c55e"},
    ])

@router.get("/recent", response_model=APIResponse[Any])
def get_recent_investigations(current_user: User = Depends(get_current_user)) -> Any:
    """Mock endpoint for the recent investigations table."""
    return success_response([
        {"id": "INV-8901", "target": "urgent-login-verify.com", "type": "URL", "status": "Completed", "risk": "High"},
        {"id": "INV-8900", "target": "invoice-788.pdf", "type": "File", "status": "In Progress", "risk": "Unknown"},
    ])
