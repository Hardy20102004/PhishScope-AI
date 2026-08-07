# BUG-001: Duplicate Router Mounts

**Severity**: HIGH
**File**: `backend/app/api/router.py`
**Discovered**: 2026-08-05
**Fixed**: 2026-08-05

---

## Description

Two routers were registered twice in the FastAPI application router at different
positions in `router.py`. FastAPI silently accepts duplicate `include_router()` calls
but this creates ambiguous routing — the last registration always wins, making the
earlier route unreachable and producing confusing Swagger UI documentation with
duplicate entries.

## Affected Routers

| Router | First Mount (Line) | Second Mount (Line) |
|--------|--------------------|---------------------|
| `digital_twin.router` | Line 100 (prefix: `/digital-twin`) | Line 152 (prefix: `/digital-twin`) |
| `cyber_resilience.router` | Line 117 (prefix: `/cyber-resilience`) | Line 154 (prefix: `/cyber-resilience`) |

Additionally, `digital_twin` was imported **twice** in the `from app.api.routers import ...`
statement on line 43 — once at the correct position and once appended at the end.

## Root Cause

The router file grew very large (160+ lines) with 100+ router registrations appended
across multiple development sessions. When the `digital_twin` and `cyber_resilience`
modules were added, they were inadvertently appended to both the import line and the
registration block, without noticing they had already been registered earlier.

## Impact

- **Swagger UI**: Both prefixes appear twice in `/api/v1/openapi.json`, confusing
  frontend developers and API consumers.
- **Route Resolution**: FastAPI registers both sets of routes. The second registration
  overwrites handlers for shared path conflicts, making the first registration's unique
  routes unreachable.
- **OpenAPI Schema**: Duplicate tag names in the generated schema can break client
  code generators.

## Fix Applied

```diff
# In the import line (line 43):
- from app.api.routers import ... cyber_fusion, orchestration, digital_twin, predictive_risk
+ from app.api.routers import ... cyber_fusion, orchestration, predictive_risk

# In the registration block (lines 150-158):
- api_router.include_router(digital_twin.router, prefix="/digital-twin", tags=["Cyber Digital Twin (DIGITAL_TWIN)"])
  api_router.include_router(predictive_risk.router, prefix="/predictive-risk", tags=["Predictive Cyber Risk (PREDICTIVE_RISK)"])
- api_router.include_router(cyber_resilience.router, prefix="/cyber-resilience", tags=["Cyber Resilience & BCP (CYBER_RESILIENCE)"])
```

The two duplicate registrations at lines 152 and 154 were removed. The original
registrations at lines 100 and 117 remain intact.

## Prevention

Consider refactoring `router.py` to use auto-discovery (e.g., scanning `app/api/routers/`
for modules) rather than manual registration. A linter check for duplicate `include_router`
calls with the same prefix would also catch this class of bug automatically.

---

*See also: [IMPROVEMENT-001_startup_checks.md](./IMPROVEMENT-001_startup_checks.md) — startup validation*
