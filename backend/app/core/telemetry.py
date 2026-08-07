import json
import logging
import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("phoenix.telemetry")

class TelemetryMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        trace_id = str(uuid.uuid4())
        request.state.trace_id = trace_id
        
        start_time = time.time()
        
        response = None
        try:
            response = await call_next(request)
        except Exception as e:
            # Capture exceptions here if needed
            raise e
        finally:
            process_time_ms = (time.time() - start_time) * 1000
            status_code = response.status_code if response else 500
            
            # Extract tenant_id or user_id from state if populated by auth middleware
            # For now, we mock tenant_id as we might not have it in middleware easily without token parsing
            tenant_id = getattr(request.state, "tenant_id", "unknown")
            
            log_data = {
                "trace_id": trace_id,
                "tenant_id": tenant_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": status_code,
                "duration_ms": round(process_time_ms, 2)
            }
            
            # Emit structured JSON log (simulating an OpenTelemetry span output or ELK stack log)
            logger.info(json.dumps(log_data))

        return response
