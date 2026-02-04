"""
UI Service - Generates UI plans based on safety verdicts.
Determines which components to show and what restrictions to apply.
"""
from typing import Any, Dict, List


def generate_ui_plan(verdict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a UI plan based on the safety verdict.
    
    Returns:
    - components: list of UI components to render
    - restrictions: dict of UI restrictions
    """
    # Default components for safe APIs
    components = ["EndpointList", "RequestBuilder", "ResponseViewer"]
    
    restrictions = {
        "execute_requests": True,
        "edit_payloads": True,
        "show_sensitive_fields": True,
        "editable_fields": []
    }
    
    # Threat detected - read-only mode
    if verdict.get("threat", False):
        components = ["EndpointList", "SafetyInspector"]
        restrictions = {
            "execute_requests": False,
            "edit_payloads": False,
            "show_sensitive_fields": False,
            "editable_fields": []
        }
        return {"components": components, "restrictions": restrictions}
    
    # Sensitive request - restrict execution
    if verdict.get("sensitive_request", False):
        restrictions["execute_requests"] = False
        restrictions["show_sensitive_fields"] = False
        if "SafetyInspector" not in components:
            components.append("SafetyInspector")
    
    # Urgency - add warning but allow interaction
    if verdict.get("urgency", False):
        if "SafetyInspector" not in components:
            components.append("SafetyInspector")
    
    return {
        "components": components,
        "restrictions": restrictions
    }


def get_conservative_ui_plan() -> Dict[str, Any]:
    """Return a fail-closed conservative UI plan."""
    return {
        "components": ["SafetyInspector"],
        "restrictions": {
            "execute_requests": False,
            "edit_payloads": False,
            "show_sensitive_fields": False,
            "editable_fields": []
        }
    }
