import asyncio
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def create_admin():
    db = SessionLocal()
    user = db.query(User).filter(User.email == "admin@phishscope.com").first()
    if not user:
        user = User(
            email="admin@phishscope.com",
            hashed_password=get_password_hash("password123"),
            full_name="Admin User",
            is_superuser=True,
            is_active=True
        )
        db.add(user)
        db.commit()
        print("Created admin user!")
    else:
        print("Admin user already exists!")
    db.close()

create_admin()
