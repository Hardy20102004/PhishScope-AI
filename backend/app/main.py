from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.exceptions import (
    PhoenixException,
    phoenix_exception_handler,
    unhandled_exception_handler,
)
from app.core.logging import setup_logging
from app.middleware.request_context import RequestContextMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    import structlog
    logger = structlog.get_logger("phoenix.main")
    logger.info("application_startup", env=settings.ENVIRONMENT, version=settings.VERSION)
    yield
    logger.info("application_shutdown")

def create_app() -> FastAPI:
    """
    Application Factory for PHOENIX backend.
    Initializes configuration, logging, exception handlers, and routing.
    """
    # Setup structured logging
    setup_logging(debug=settings.DEBUG)
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        description="Core API for the AI-Powered Digital Scam Investigation Platform",
        lifespan=lifespan,
    )

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS] if settings.BACKEND_CORS_ORIGINS else ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Custom Middlewares
    app.add_middleware(RequestContextMiddleware)

    # Exception Handlers
    app.add_exception_handler(PhoenixException, phoenix_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    # Routers
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app

app = create_app()
