import sys
import os
import asyncio
sys.path.append(os.getcwd())
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.db.session import SessionLocal
from backend.app.models.user import User

client = TestClient(app)

# Find a user to authenticate as
db = SessionLocal()
user = db.query(User).first()
if not user:
    print("No users found in database.")
    sys.exit(1)

# We need a token for the user. We can bypass auth or generate a token.
from backend.app.core.security import create_access_token
from datetime import timedelta
token = create_access_token(user.id, expires_delta=timedelta(minutes=15))

headers = {"Authorization": f"Bearer {token}"}
payload = {"target": "youtube.com", "type": "WEBSITE"}

response = client.post("/api/v1/investigations/", json=payload, headers=headers)
print("Status Code:", response.status_code)
print("Response:", response.json())
