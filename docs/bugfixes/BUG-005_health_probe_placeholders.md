# BUG-005: Health Check Always Reports "disconnected"

**Severity**: MEDIUM
**File**: `backend/app/api/v1/endpoints/health.py`
**Discovered**: 2026-08-05
**Fixed**: 2026-08-05

---

## Description

The `/api/v1/health` endpoint — used by Kubernetes liveness and readiness probes —
always returned hardcoded placeholder values regardless of actual system state:

```python
data = HealthResponse(
    status="healthy",
    database="disconnected",  # Placeholder
    cache="disconnected"      # Placeholder
)
```

This means:
- The health endpoint **always returned HTTP 200** even when the database was down.
- Kubernetes readiness probes would **never detect database failures**.
- Operators monitoring the health endpoint would see misleading status information.

## Root Cause

The endpoint was written as a stub during initial project setup. The comment
`# Placeholder` was left in the code, indicating the real implementation was
deferred and never revisited.

## Impact

- **Kubernetes**: Readiness probes never fail on DB failure, so the pod receives
  traffic even when it cannot serve real requests, causing cascading errors.
- **Liveness probes**: Would never restart a pod even when completely broken.
- **Monitoring dashboards**: Would show "healthy" for a broken system.
- **On-call engineers**: Would have no automated alerting on infrastructure failures.

## Fix Applied

Replaced the stubs with actual probes:

### Database Probe
```python
def _check_database(db: Session) -> str:
    try:
        db.execute(text("SELECT 1"))
        return "connected"
    except Exception:
        return "disconnected"
```

Uses the existing SQLAlchemy session (injected via dependency) to run a
minimal `SELECT 1` query. No additional connections are opened.

### Redis Probe
```python
def _check_redis() -> str:
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        return "not_configured"
    try:
        import redis as redis_lib
        client = redis_lib.from_url(redis_url, socket_connect_timeout=2)
        client.ping()
        return "connected"
    except Exception:
        return "disconnected"
```

Reads `REDIS_URL` from the environment. Returns `"not_configured"` gracefully
if Redis is not set up (e.g., during local development without Docker).
Uses a 2-second connection timeout to prevent the health endpoint from hanging.

### Overall Status Logic
```python
overall = "healthy" if db_status == "connected" else "degraded"
```

The endpoint now returns `"degraded"` status when the database is unreachable,
which can be used to fail Kubernetes readiness probes while still allowing
liveness probes to pass (keeping the pod alive for debugging).

## Kubernetes Configuration Recommendation

```yaml
readinessProbe:
  httpGet:
    path: /api/v1/health
    port: 8000
  failureThreshold: 3
  periodSeconds: 10
livenessProbe:
  httpGet:
    path: /api/v1/health
    port: 8000
  failureThreshold: 5
  periodSeconds: 30
```
