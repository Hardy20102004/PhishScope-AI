from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class SecureHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Enforce HTTP Strict Transport Security
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        
        # Prevent Clickjacking
        response.headers["X-Frame-Options"] = "DENY"
        
        # Prevent MIME-sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # Enforce Content Security Policy (strict basic policy for API)
        response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
        
        # Cross-Site Scripting (XSS) Protection
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Prevent browser from sending referrer to unencrypted sites
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        return response
