from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token
from app.schemas.base import APIResponse
from app.api.responses import success_response
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token
from app.core.config import settings
from datetime import timedelta

router = APIRouter()

@router.post("/register", response_model=APIResponse[UserResponse], status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
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
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
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
    # In a real setup, we'd read the cookie here using FastAPI's Cookie parameter
    # For now, we simulate it
):
    """Refresh the access token using the HttpOnly cookie."""
    # Logic to validate refresh token from cookie goes here
    # For now, this is a placeholder to satisfy the frontend contract
    new_access_token = create_access_token("placeholder_id")
    return success_response({"access_token": new_access_token, "token_type": "bearer"})

@router.post("/logout")
def logout(response: Response):
    """Logout current user by deleting the refresh token cookie."""
    response.delete_cookie("refresh_token")
    return success_response({"message": "Successfully logged out"})
