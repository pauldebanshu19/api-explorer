import json
import logging
import traceback
from typing import Callable
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("policy-aware-api")


def get_conservative_error_response() -> dict:
    """Return fail-closed response for unhandled errors."""
    return {
        "verdict": {
            "urgency": True,
            "threat": False,
            "sensitive_request": True,
            "execution_risk": True,
            "data_exposure_risk": True,
            "policy_explanation": "internal error — conservative block applied"
        },
        "ui_contract": {
            "components": ["SafetyInspector"],
            "restrictions": {
                "execute_requests": False,
                "edit_payloads": False,
                "show_sensitive_fields": False,
                "schema_detail": "hidden"
            },
            "warnings": ["System error - all actions blocked for safety"],
            "blocked": True
        }
    }


class ErrorMiddleware(BaseHTTPMiddleware):
    """Converts crashes into conservative fail-closed responses."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
        except Exception as e:
            # Log the error
            logger.error(json.dumps({
                "event": "error",
                "path": request.url.path,
                "error": str(e),
                "traceback": traceback.format_exc()
            }))
            
            # For /analyze endpoint, return conservative verdict
            if "/analyze" in request.url.path:
                return JSONResponse(
                    status_code=200,
                    content=get_conservative_error_response()
                )
            
            # For other endpoints, return generic error
            return JSONResponse(
                status_code=500,
                content={"error": "Internal server error", "blocked": True}
            )
