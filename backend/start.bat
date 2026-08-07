@echo off
setlocal

echo Running database migrations...
alembic upgrade head
if %errorlevel% neq 0 (
    echo Migration failed.
    exit /b %errorlevel%
)

echo Starting FastAPI server via Uvicorn...
uvicorn app.main:app --host 0.0.0.0 --port 8000 --proxy-headers
