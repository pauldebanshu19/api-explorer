import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Configure logging to show in terminal
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("api")


class LoggingMiddleware(BaseHTTPMiddleware):
    """Logs every request for observability."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration_ms = (time.time() - start_time) * 1000
        
        # Log to terminal
        client = request.client.host if request.client else "unknown"
        print(f"[API] {request.method} {request.url.path} -> {response.status_code} ({duration_ms:.0f}ms) from {client}")
        
        return response
