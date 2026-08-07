$ErrorActionPreference = "Stop"

Write-Host "Running database migrations..."
alembic upgrade head

Write-Host "Starting FastAPI server via Uvicorn..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --proxy-headers
