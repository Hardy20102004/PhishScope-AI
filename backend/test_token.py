import sys
import uuid
import logging
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import create_access_token
from app.api.deps import get_current_user
import jwt
from app.core.config import settings

db = SessionLocal()
user = db.query(User).first()
if not user:
    print("No user found.")
    sys.exit(0)

token = create_access_token(user.id)
print(f"Token: {token}")

try:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    print(f"Payload: {payload}")
    user_id = payload.get("sub")
    user_uuid = uuid.UUID(user_id)
    u = db.query(User).filter(User.id == user_uuid).first()
    print(f"User validated: {u.email}")
except Exception as e:
    print(f"Error: {e}")
