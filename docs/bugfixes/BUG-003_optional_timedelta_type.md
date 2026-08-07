# BUG-003: Missing Optional[timedelta] Type Annotation

**Severity**: HIGH
**File**: `backend/app/core/security.py`
**Discovered**: 2026-08-05
**Fixed**: 2026-08-05

---

## Description

Both `create_access_token()` and `create_refresh_token()` declared their `expires_delta`
parameter with a bare type of `timedelta` and a default value of `None`:

```python
def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
```

Using `None` as the default for a non-Optional typed parameter is a type error. Python
does not raise a runtime error for this in 3.10+ due to deferred annotation evaluation,
but static type checkers (mypy, pyright) correctly flag this as invalid.

## Root Cause

The `Optional` wrapper was omitted when the function signature was originally written.
This is a common mistake when porting from Python 2-era code or writing quickly without
running a type checker.

## Impact

- **mypy / pyright strict mode**: Both tools report `error: Incompatible default for argument "expires_delta"`.
- **Runtime**: No immediate crash, but if a caller passes `expires_delta=None` explicitly
  (which is valid Python), static analysis tools would incorrectly flag the call site as
  an error, leading developers to add unnecessary casts or workarounds.
- **Code Clarity**: Reading the signature, a developer might assume `None` is not a
  valid value, and always provide a delta — preventing the default token lifetime logic
  from running.

## Fix Applied

```diff
- from typing import Any, Union
+ from typing import Any, Optional, Union

- def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
+ def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:

- def create_refresh_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
+ def create_refresh_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
```

## Verification

After the fix, running `mypy backend/app/core/security.py --strict` should produce
zero errors on these function signatures.
