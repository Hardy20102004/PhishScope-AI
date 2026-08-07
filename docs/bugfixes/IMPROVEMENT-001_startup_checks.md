# IMPROVEMENT-001: Startup Validation Checks

**Severity**: MEDIUM
**File**: `backend/app/core/startup_checks.py`, `backend/app/main.py`
**Discovered**: 2026-08-05
**Fixed**: 2026-08-05

---

## Description

The FastAPI backend would attempt to start up even if critical environment variables were missing, the database was entirely unreachable, or the `SECRET_KEY` was insecure.

These misconfigurations would only manifest as runtime errors (500s) when users attempted to interact with the API, making debugging extremely difficult in Kubernetes environments where container logs are the primary diagnostic tool.

## Implementation

Created a new dedicated module `startup_checks.py` designed to run in the FastAPI lifespan context manager (before the server binds to the port and accepts traffic).

### Checks Implemented

1. **Required Environment Variables**:
   - Asserts that `SECRET_KEY` and `SQLALCHEMY_DATABASE_URI` are present.
   - Raises `RuntimeError` immediately if missing in non-dev environments.

2. **Secret Key Strength**:
   - Validates that the default key (`"CHANGE_THIS_IN_PRODUCTION"`) is not used in production.
   - Raises `RuntimeError` if violated.
   - Logs a warning if the provided key is shorter than 64 hex characters (256 bits).

3. **Database Reachability**:
   - Uses SQLAlchemy `create_engine` to issue a fast `SELECT 1` against the configured database URI.
   - **Does not raise an exception** on failure, but logs a clear warning. This allows the API to start in "degraded" mode, relying on the `/health` endpoint and Kubernetes readiness probes to block traffic while the database finishes booting.

## Integration

Wired into `main.py` using the FastAPI `@asynccontextmanager` lifespan feature:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    import structlog
    from app.core.startup_checks import run_all_checks
    logger = structlog.get_logger("phoenix.main")

    # Run fail-fast validation before accepting any traffic
    run_all_checks(settings)

    logger.info("application_startup", env=settings.ENVIRONMENT, version=settings.VERSION)
    yield
    logger.info("application_shutdown")
```

## Impact

- Drastically reduced debugging time during deployments.
- "Fail-fast" philosophy prevents the app from running in an insecure state.
