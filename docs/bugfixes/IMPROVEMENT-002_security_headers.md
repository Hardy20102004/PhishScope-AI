# IMPROVEMENT-002: Security Header Consolidation

**Severity**: MEDIUM
**File**: `backend/app/middleware/request_context.py`
**Discovered**: 2026-08-05
**Fixed**: 2026-08-05

---

## Description

The project contained a `SecureHeadersMiddleware` class in `security_headers.py`, but this middleware was never added to the FastAPI application via `app.add_middleware()`. It was effectively dead code.

Meanwhile, the active `RequestContextMiddleware` applied a few basic security headers, but was missing critical modern web protections like Content Security Policy (CSP) and Referrer Policy.

## Fix Applied

Instead of adding another layer of middleware, the dead headers from `SecureHeadersMiddleware` were ported directly into `RequestContextMiddleware`, consolidating all header injection into a single pass.

Added Headers:
- `Content-Security-Policy: default-src 'none'; frame-ancestors 'none'`
  - Highly restrictive CSP appropriate for a pure JSON API. Prevents the API from being embedded in frames, or executing any unexpected scripts if an endpoint accidentally returns HTML content type.
- `Referrer-Policy: strict-origin-when-cross-origin`
  - Standard privacy protection preventing sensitive URL paths from leaking in the Referer header to external sites.
- `Permissions-Policy: geolocation=(), camera=(), microphone=()`
  - Explicitly disables powerful browser features, reducing the attack surface.
- `X-XSS-Protection: 1; mode=block`
  - Legacy protection for older browsers.

Additionally, the `X-Process-Time` logging and header were updated to output human-readable milliseconds (e.g., `14.23ms`) instead of raw unrounded seconds (`0.014234066009521484`).

```python
# ── Security Headers ─────────────────────────────────────────────────
response.headers["X-Content-Type-Options"] = "nosniff"
response.headers["X-Frame-Options"] = "DENY"
response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
response.headers["X-XSS-Protection"] = "1; mode=block"
# ─────────────────────────────────────────────────────────────────────
```

## Cleanup

The `security_headers.py` file can now be safely deleted in a future cleanup pass, as its functionality is fully subsumed by `request_context.py`.
