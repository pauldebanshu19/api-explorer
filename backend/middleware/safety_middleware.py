"""
Safety Middleware - Logs and handles unsafe requests.
"""
import json
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("safety-middleware")


class SafetyMiddleware(BaseHTTPMiddleware):
    """Middleware to log requests flagged as potentially unsafe."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        # Check for suspicious headers or patterns
        user_agent = request.headers.get("user-agent", "")
        
        # Log suspicious user agents
        suspicious_patterns = ["curl", "wget", "python-requests", "PostmanRuntime"]
        is_suspicious = any(pattern.lower() in user_agent.lower() for pattern in suspicious_patterns)
        
        if is_suspicious:
            logger.warning(json.dumps({
                "event": "suspicious_request",
                "path": str(request.url.path),
                "method": request.method,
                "user_agent": user_agent,
                "client_ip": request.client.host if request.client else "unknown"
            }))
        
        # Continue processing
        response = await call_next(request)
        return response
