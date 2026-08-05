# BUG-006: Missing SECRET_KEY Guard & Pydantic v2 Postgres API Bug

**Severity**: CRITICAL
**File**: `backend/app/core/config.py`
**Discovered**: 2026-08-05
**Fixed**: 2026-08-05

---

## Description

This file contained two distinct severe issues:

1. **Weak Default Secret Key**: The `SECRET_KEY` was hardcoded to `"CHANGE_THIS_IN_PRODUCTION"` and there was no validation preventing the app from starting up with this insecure default in production environments.
2. **Broken Postgres Connection String**: The `PostgresDsn.build()` call used the `user=` parameter, which was deprecated and removed in Pydantic v2 (renamed to `username=`). This caused the assembly function to fail silently and fall back to the SQLite test database string `sqlite:///./phoenix_test.db` even when Postgres environment variables were provided.

## Impact

- **Security (SECRET_KEY)**: A default secret key allows attackers to forge valid JWTs, completely bypassing authentication (JWT spoofing attack).
- **Data Integrity (PostgresDsn)**: The application would start, but all data would be written to a local ephemeral SQLite file (`phoenix_test.db`) inside the Docker container instead of the managed PostgreSQL database. All data would be lost when the container restarted.

## Fix Applied

### 1. SECRET_KEY Guard

Added a Pydantic `model_validator` to enforce a strong secret key in non-dev environments:

```python
_DEFAULT_SECRET = "CHANGE_THIS_IN_PRODUCTION"

@model_validator(mode="after")
def _guard_secret_key(self) -> "Settings":
    if self.ENVIRONMENT != "development" and self.SECRET_KEY == _DEFAULT_SECRET:
        raise ValueError(
            "CRITICAL: SECRET_KEY must be changed from the default value in non-development environments. "
            "Set a strong random SECRET_KEY in your .env file before deploying."
        )
    return self
```

### 2. Pydantic v2 PostgresDsn Fix

Updated the `assemble_db_connection` logic to use the correct `username` parameter and wrap the result in `str()`:

```python
# Before
return PostgresDsn.build(
    scheme="postgresql",
    user=values.get("POSTGRES_USER"),
    password=values.get("POSTGRES_PASSWORD"),
    host=values.get("POSTGRES_SERVER"),
    path=f"/{values.get('POSTGRES_DB') or ''}",
)

# After
return str(PostgresDsn.build(
    scheme="postgresql",
    username=values.get("POSTGRES_USER"),
    password=values.get("POSTGRES_PASSWORD"),
    host=server,
    path=values.get("POSTGRES_DB") or "",
))
```
