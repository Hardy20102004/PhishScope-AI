#!/usr/bin/env python3
"""
seed_db.py — Creates all tables and seeds the admin user.
Run from the backend/ directory with the venv activated:
    python seed_db.py
"""
import sys
import os

# Ensure we're in the backend dir
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.base import Base       # imports ALL models
from app.db.session import engine, SessionLocal
from app.models.user import User
from app.core.security import get_password_hash
from app.core.config import settings

print("=" * 55)
print("  PhishScope AI — Database Setup")
print("=" * 55)
print(f"  DB URI : {settings.SQLALCHEMY_DATABASE_URI}")
print(f"  Tables : {len(Base.metadata.tables)} defined")

# ── 1. Create all tables ──────────────────────────────────────────────
print("\n  [1/2] Creating database tables...")
Base.metadata.create_all(bind=engine)
print("        ✓ Done")

# ── 2. Seed admin user ────────────────────────────────────────────────
print("\n  [2/2] Seeding admin user...")
admin_email    = os.getenv("ADMIN_EMAIL",    "admin@phoenix.ai")
admin_password = os.getenv("ADMIN_PASSWORD", "Phoenix@Admin123")

db = SessionLocal()
try:
    existing = db.query(User).filter(User.email == admin_email).first()
    if existing:
        print(f"        ✓ Admin already exists: {admin_email}")
        # Make sure password is up-to-date
        existing.hashed_password = get_password_hash(admin_password)
        existing.is_active = True
        existing.is_superuser = True
        db.commit()
        print("        ✓ Password & flags refreshed")
    else:
        admin = User(
            email=admin_email,
            hashed_password=get_password_hash(admin_password),
            full_name="Phoenix Admin",
            is_superuser=True,
            is_active=True,
        )
        db.add(admin)
        db.commit()
        print(f"        ✓ Created admin: {admin_email}")
finally:
    db.close()

print()
print("=" * 55)
print("  ✅  Database ready!")
print(f"  Email    : {admin_email}")
print(f"  Password : {admin_password}")
print("=" * 55)
