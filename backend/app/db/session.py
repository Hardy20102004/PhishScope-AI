from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Determine if we are using SQLite (for local/tests) or Postgres
connect_args = {"check_same_thread": False} if "sqlite" in str(settings.SQLALCHEMY_DATABASE_URI) else {}

engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
