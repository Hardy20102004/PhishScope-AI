# BUG-002: Authentication Bypass via Broken Refresh Token Endpoint

**Severity**: CRITICAL
**File**: `backend/app/api/v1/endpoints/auth.py`
**Discovered**: 2026-08-05
**Fixed**: 2026-08-05
**CVE Class**: Authentication Bypass / Broken Auth (OWASP A07:2021)

---

## Description

The `/api/v1/auth/refresh` endpoint — responsible for issuing new access tokens
using a user's HttpOnly refresh token cookie — was a non-functional placeholder
that issued valid signed JWTs for a hardcoded fake user ID (`"placeholder_id"`)
without reading or validating any cookie or credentials.

## Vulnerable Code (Before Fix)

```python
@router.post("/refresh", response_model=APIResponse[Token])
def refresh_token(
    response: Response,
    db: Session = Depends(get_db),
    # In a real setup, we'd read the cookie here using FastAPI's Cookie parameter
    # For now, we simulate it
):
    """Refresh the access token using the HttpOnly cookie."""
    # Logic to validate refresh token from cookie goes here
    # For now, this is a placeholder to satisfy the frontend contract
    new_access_token = create_access_token("placeholder_id")
    return success_response({"access_token": new_access_token, "token_type": "bearer"})
```

## Attack Scenario

Any anonymous user could send a POST request to `/api/v1/auth/refresh` without
any credentials or cookies and receive a valid, signed JWT access token in return:

```bash
curl -X POST http://api.phoenix-platform.com/api/v1/auth/refresh
# Response: {"status":"success","data":{"access_token":"eyJhbG...","token_type":"bearer"}}
```

This token would then be accepted by `deps.py`'s `get_current_user()` as a real
authenticated session. Because the sub claim was `"placeholder_id"` (not a valid UUID),
this would trigger a secondary bug (BUG-007) causing a 500 rather than actually
authenticating — but the vulnerability existed in its raw form.

## Root Cause

The endpoint was intentionally left as a stub during early development with a comment
noting that the real implementation was pending. It was never replaced before the
codebase was pushed to the repository.

## Impact

- **CRITICAL**: Any unauthenticated user could obtain a signed JWT from the system.
- Even though the UUID parsing bug (BUG-007) prevented full exploitation in the current
  state, fixing BUG-007 without fixing this bug would have enabled a full authentication
  bypass.
- The two bugs compounded each other in a way that masked this vulnerability in basic
  testing.

## Fix Applied

The endpoint now:

1. Reads the HttpOnly `refresh_token` cookie via FastAPI's `Cookie(default=None)` dependency.
2. Decodes and verifies the JWT signature using the application's `SECRET_KEY`.
3. Validates the `type` claim equals `"refresh"` (rejects access tokens used as refresh tokens).
4. Parses the `sub` claim as a UUID — returns 401 on failure.
5. Queries the database to verify the user exists and is active.
6. Only if all checks pass, issues a new access token.

```python
@router.post("/refresh", response_model=APIResponse[Token])
def refresh_token(
    response: Response,
    db: Session = Depends(get_db),
    refresh_token: str = Cookie(default=None),  # Read real cookie
):
    invalid_exc = HTTPException(status_code=401, detail="Invalid or expired refresh token.")

    if not refresh_token:
        raise invalid_exc

    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        token_type = payload.get("type")
        if not user_id or token_type != "refresh":
            raise invalid_exc
    except jwt.PyJWTError:
        raise invalid_exc

    user = db.query(User).filter(User.id == uuid.UUID(user_id)).first()
    if not user or not user.is_active:
        raise invalid_exc

    return success_response({"access_token": create_access_token(user.id), "token_type": "bearer"})
```

## Recommendations

- Add integration tests covering: (a) missing cookie, (b) expired token, (c) wrong
  token type, (d) non-existent user, (e) inactive user.
- Consider rotating the refresh token on each use (refresh token rotation pattern)
  to detect replay attacks.
- Add rate limiting on this endpoint to prevent brute-force attempts.

---

*Related: [BUG-007_uuid_runtime_crash.md](./BUG-007_uuid_runtime_crash.md) — compound bug*
