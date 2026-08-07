"""
startup_checks.py
-----------------
Startup sanity-check hooks for the PHOENIX backend.
Called during the lifespan context manager BEFORE the app accepts traffic.

Raises RuntimeError on any critical misconfiguration so that the process
crashes immediately (fail-fast) rather than serving requests with a broken config.
"""
import os
import structlog

logger = structlog.get_logger("phoenix.startup")

_DEFAULT_SECRET = "CHANGE_THIS_IN_PRODUCTION"
_MIN_SECRET_KEY_LEN = 64  # 256-bit minimum (hex encoded)


def check_secret_key(secret_key: str, environment: str) -> None:
    """
    Ensure the SECRET_KEY is sufficiently strong.
    - In non-development environments, block the default insecure value.
    - In all environments, warn if the key is suspiciously short.
    """
    if secret_key == _DEFAULT_SECRET and environment != "development":
        raise RuntimeError(
            "CRITICAL STARTUP FAILURE: SECRET_KEY is set to the default insecure value. "
            "Generate a strong key with: python -c \"import secrets; print(secrets.token_hex(64))\" "
            "and set it as SECRET_KEY in your .env file."
        )
    if len(secret_key) < _MIN_SECRET_KEY_LEN:
        logger.warning(
            "weak_secret_key",
            message=(
                "SECRET_KEY appears shorter than recommended 256 bits. "
                "Consider regenerating with: secrets.token_hex(64)"
            ),
        )


def check_database_reachable(database_uri: str) -> None:
    """
    Attempt a real database connection at startup.
    Logs a warning (not a crash) so the app can still start in degraded mode
    if the DB is warming up. Kubernetes readiness probes will block traffic.
    """
    try:
        from sqlalchemy import create_engine, text
        connect_args = {"check_same_thread": False} if "sqlite" in database_uri else {}
        engine = create_engine(database_uri, connect_args=connect_args, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("startup_db_check", status="connected", uri_scheme=database_uri.split("://")[0])
    except Exception as exc:
        logger.warning(
            "startup_db_check",
            status="unreachable",
            error=str(exc),
            advice="The database is not reachable. Check SQLALCHEMY_DATABASE_URI / POSTGRES_* env vars.",
        )


def check_required_env_vars() -> None:
    """
    Validate that required environment variables are present.
    Raises RuntimeError if any required variable is missing in non-dev environments.
    """
    required_in_production = [
        "SECRET_KEY",
        "SQLALCHEMY_DATABASE_URI",
    ]
    environment = os.getenv("ENVIRONMENT", "development")
    if environment == "development":
        return  # Be lenient in dev

    missing = [var for var in required_in_production if not os.getenv(var)]
    if missing:
        raise RuntimeError(
            f"CRITICAL STARTUP FAILURE: Missing required environment variables for '{environment}' environment: "
            + ", ".join(missing)
        )


def run_all_checks(settings) -> None:
    """
    Entry point called from the lifespan context manager.
    Runs all startup validation checks in order.
    """
    logger.info("startup_checks_begin", environment=settings.ENVIRONMENT)
    check_required_env_vars()
    check_secret_key(settings.SECRET_KEY, settings.ENVIRONMENT)
    check_database_reachable(settings.SQLALCHEMY_DATABASE_URI)
    logger.info("startup_checks_passed")
