# Stage 1: Build dependencies
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -r requirements.txt

# Stage 2: Final runtime image
FROM python:3.11-slim

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Install runtime dependencies (like libpq for psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy pre-built wheels from builder
COPY --from=builder /build/wheels /wheels
RUN pip install --no-cache /wheels/* && rm -rf /wheels

# Copy application code
COPY ./app /app/app
COPY ./alembic /app/alembic
COPY alembic.ini /app/
COPY start.sh /app/

# Set proper ownership
RUN chown -R appuser:appuser /app && chmod +x /app/start.sh

# Switch to non-root user
USER appuser

# Expose API port
EXPOSE 8000

# Run FastAPI
CMD ["/app/start.sh"]
