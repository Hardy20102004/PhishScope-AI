
import uuid

import jwt
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.responses import success_response
from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
)
from app.models.user import User
from app.schemas.base import APIResponse
from app.schemas.user import Token, UserCreate, UserResponse

router = APIRouter()

@router.post("/register", response_model=APIResponse[UserResponse], status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system",
        )
    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return success_response(user)

@router.post("/login", response_model=APIResponse[Token])
def login(
    response: Response,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """OAuth2 compatible token login, getting an access token for future requests."""
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    # Set HttpOnly cookie for the refresh token
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True if settings.ENVIRONMENT == "production" else False,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )

    return success_response({"access_token": access_token, "token_type": "bearer"})

@router.post("/refresh", response_model=APIResponse[Token])
def refresh_token(
    response: Response,
    db: Session = Depends(get_db),
    refresh_token: str = Cookie(default=None),
):
    """
    Refresh the access token using the HttpOnly refresh token cookie.
    Validates the cookie's JWT, confirms the user still exists and is active,
    then issues a fresh access token.
    """
    invalid_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token. Please log in again.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not refresh_token:
        raise invalid_exc

    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        if not user_id or token_type != "refresh":
            raise invalid_exc
    except jwt.PyJWTError:
        raise invalid_exc

    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise invalid_exc

    user = db.query(User).filter(User.id == user_uuid).first()
    if not user or not user.is_active:
        raise invalid_exc

    new_access_token = create_access_token(user.id)
    return success_response({"access_token": new_access_token, "token_type": "bearer"})

@router.post("/logout")
def logout(response: Response):
    """Logout current user by deleting the refresh token cookie."""
    response.delete_cookie("refresh_token")
    return success_response({"message": "Successfully logged out"})

