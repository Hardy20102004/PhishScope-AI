# BUG-004: Hardcoded Developer Machine Path in requirements.txt

**Severity**: CRITICAL (Portability)
**File**: `backend/requirements.txt`
**Discovered**: 2026-08-05
**Fixed**: 2026-08-05

---

## Description

Line 40-41 of `requirements.txt` contained:

```
# Editable install with no version control (phoenix-backend==0.1.0)
-e "/Users/umeshgupta/PhishScope AI/backend"
```

This is a pip editable install directive pointing to the **original developer's Mac
home directory**. This path does not exist on any other machine.

## Root Cause

When `pip freeze` is run in a virtualenv that has an editable (development mode)
package installed, pip writes the `-e` directive to the frozen requirements output.
The developer ran `pip freeze > requirements.txt` without removing this artifact before
committing.

## Impact

- **Any CI/CD pipeline** running `pip install -r requirements.txt` would fail with:
  ```
  ERROR: /Users/umeshgupta/PhishScope AI/backend does not exist.
  ```
- **Any contributor** setting up the project from scratch would get a broken install.
- **Docker builds** using this requirements file would fail during the `pip install`
  step, making the Dockerfile non-functional.
- **Deployment pipelines** (Kubernetes, cloud runners) would also fail.

## Fix Applied

```diff
- # Editable install with no version control (phoenix-backend==0.1.0)
- -e "/Users/umeshgupta/PhishScope AI/backend"
  pillow==12.3.0
```

The editable install line and its comment were removed. The package itself (`phoenix-backend`)
is installed via `pyproject.toml` in the backend directory, which pip will use
automatically when running `pip install -e .` from within the `backend/` directory.

## Prevention

Add the following to your `pip freeze` workflow:

```bash
# Freeze dependencies, excluding editable installs
pip freeze | grep -v "^-e" > requirements.txt
```

Or use `pip-tools` (`pip-compile`) which handles this correctly by default.
