# BUG-007: Unguarded uuid.UUID() Causes 500 Runtime Crash

**Severity**: HIGH
**File**: `backend/app/api/deps.py`
**Discovered**: 2026-08-05
**Fixed**: 2026-08-05

---

## Description

In the `get_current_user` dependency, the `user_id` parsed from the JWT `sub` claim
was passed directly to `uuid.UUID()` without a try/except block:

```python
user = db.query(User).filter(User.id == uuid.UUID(user_id)).first()
```

If the JWT was well-formed and successfully decoded, but the `sub` claim was not a valid
UUID format string, the `uuid.UUID()` constructor would raise a `ValueError`. Because
this exception was unhandled, FastAPI returned a generic `500 Internal Server Error`
instead of properly rejecting the authentication attempt with a `401 Unauthorized`.

## Impact

- Any request containing a valid JWT but malformed `sub` claim caused a 500 error.
- This compounded heavily with BUG-002, where the broken `/refresh` endpoint issued
  JWTs with `sub="placeholder_id"`. When the frontend attempted to use these tokens,
  every authenticated route crashed with a 500 instead of triggering a proper 401
  re-authentication flow.
- A malicious actor could intentionally send malformed validly-signed tokens to flood
  application error logs or trigger monitoring alerts.

## Fix Applied

Wrapped the UUID parsing in a `try/except ValueError` block and raised the standard
`credentials_exception` (HTTP 401) on failure. Also moved the lazy `import uuid` to
the top of the file for cleanliness.

```python
import uuid

# ...

try:
    user_uuid = uuid.UUID(user_id)
except ValueError:
    # Sub claim is not a valid UUID — reject with 401, not 500
    raise credentials_exception

user = db.query(User).filter(User.id == user_uuid).first()
```

Additionally, added a check to ensure the token being used for access routes has
the `type` claim set to `"access"`, preventing refresh tokens from being used directly
against application endpoints.
