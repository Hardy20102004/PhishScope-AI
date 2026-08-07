import uuid
import datetime
from pydantic import BaseModel, ConfigDict
from app.schemas.user import UserResponse
from app.models.user import User
from app.schemas.base import APIResponse
from app.api.responses import success_response

u = User(id=uuid.uuid4(), email="test@test.com", hashed_password="123", full_name="Test", is_active=True, is_superuser=True, created_at=datetime.datetime.now(datetime.timezone.utc), updated_at=datetime.datetime.now(datetime.timezone.utc))

resp_dict = success_response(u)
try:
    obj = APIResponse[UserResponse].model_validate(resp_dict)
    print("Success")
except Exception as e:
    print(f"Failed: {e}")
