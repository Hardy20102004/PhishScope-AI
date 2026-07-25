import structlog
from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.api.responses import error_response

logger = structlog.get_logger("phoenix.exceptions")

class PhoenixException(Exception):
    """Base exception class for PHOENIX"""
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, code: str = "INTERNAL_ERROR"):
        self.message = message
        self.status_code = status_code
        self.code = code
        super().__init__(self.message)

class AuthException(PhoenixException):
    """Authentication and Authorization exceptions"""
    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED, code="UNAUTHORIZED")

class NotFoundException(PhoenixException):
    """Resource not found exception"""
    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND, code="NOT_FOUND")

async def phoenix_exception_handler(request: Request, exc: PhoenixException):
    """Global exception handler for Phoenix exceptions"""
    logger.warning("api_error", path=request.url.path, error=exc.message, status=exc.status_code)
    resp = error_response(code=exc.code, message=exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content=resp.model_dump()
    )

async def unhandled_exception_handler(request: Request, exc: Exception):
    """Fallback handler for unhandled exceptions (Internal Server Errors)"""
    logger.error("unhandled_exception", path=request.url.path, error=str(exc))
    resp = error_response(code="INTERNAL_SERVER_ERROR", message="Internal server error occurred. Please try again later.")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=resp.model_dump()
    )
