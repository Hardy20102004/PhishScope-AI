from typing import Any

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.api.responses import success_response
from app.models.user import User
from app.schemas.base import APIResponse
from app.schemas.user import UserResponse

router = APIRouter()

@router.get("/me", response_model=APIResponse[UserResponse])
def read_users_me(
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get current user profile.
    """
    return success_response(current_user)
