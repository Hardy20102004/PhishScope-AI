import time
import uuid

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = structlog.get_logger("phoenix.middleware")

class RequestContextMiddleware(BaseHTTPMiddleware):
    """
    Injects a unique request ID into each request and logs request timing.
    Also sets a comprehensive suite of security headers on every response.
    """
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)

        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(round(process_time * 1000, 2)) + "ms"
        response.headers["X-Request-ID"] = request_id

        # ── Security Headers ─────────────────────────────────────────────────
        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"
        # Enforce HTTPS for 1 year (production only — safe to apply everywhere)
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        # Content Security Policy — strict default for a pure JSON API
        response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
        # Referrer control
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        # Disable potentially dangerous browser features
        response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
        # XSS protection header (legacy browsers)
        response.headers["X-XSS-Protection"] = "1; mode=block"
        # ─────────────────────────────────────────────────────────────────────

        logger.info(
            "request_completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(process_time * 1000, 2),
        )

        return response

