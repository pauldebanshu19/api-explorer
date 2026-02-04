from typing import Any, Dict, List
import re


# Sensitive field patterns
SENSITIVE_FIELDS = [
    "card_number", "cvv", "ssn", "password", "secret", "api_key",
    "credit_card", "social_security", "bank_account", "pin", "token"
]

# Threat keywords
THREAT_KEYWORDS = [
    "exploit", "attack", "breach", "hack", "injection", "bypass",
    "unauthorized", "vulnerability", "malicious", "compromise"
]

# Urgency keywords
URGENCY_KEYWORDS = [
    "urgent", "immediate", "asap", "emergency", "critical", "now"
]


def detect_sensitive_fields(api_spec: str, constructed_input: Dict[str, Any]) -> List[str]:
    """Detect sensitive fields in API spec or input."""
    found = []
    spec_lower = api_spec.lower()
    
    for field in SENSITIVE_FIELDS:
        if field in spec_lower:
            found.append(field)
    
    # Check constructed input keys
    for key in constructed_input.keys():
        key_lower = key.lower()
        for field in SENSITIVE_FIELDS:
            if field in key_lower and field not in found:
                found.append(field)
    
    return found


def detect_threats(user_intent: str, api_spec: str) -> List[str]:
    """Detect threat signals in user intent or spec."""
    found = []
    combined = (user_intent + " " + api_spec).lower()
    
    for keyword in THREAT_KEYWORDS:
        if keyword in combined:
            found.append(keyword)
    
    return found


def detect_urgency(user_intent: str) -> bool:
    """Detect urgency signals in user intent."""
    intent_lower = user_intent.lower()
    return any(keyword in intent_lower for keyword in URGENCY_KEYWORDS)


def analyze_request(
    api_spec: str,
    user_intent: str,
    example_payloads: List[Dict[str, Any]],
    constructed_input: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Analyze an API request for safety concerns.
    
    Returns a safety verdict with:
    - urgency: bool
    - threat: bool
    - sensitive_request: bool
    - explanation: str
    """
    sensitive_fields = detect_sensitive_fields(api_spec, constructed_input)
    threats = detect_threats(user_intent, api_spec)
    urgency = detect_urgency(user_intent)
    
    # Build explanation
    explanations = []
    
    if sensitive_fields:
        explanations.append(f"Sensitive fields detected: {', '.join(sensitive_fields)}")
    
    if threats:
        explanations.append(f"Threat signals: {', '.join(threats)}")
    
    if urgency:
        explanations.append("Urgency detected in request")
    
    if not explanations:
        explanations.append("No safety concerns detected")
    
    return {
        "urgency": urgency,
        "threat": len(threats) > 0,
        "sensitive_request": len(sensitive_fields) > 0,
        "explanation": ". ".join(explanations)
    }


def get_conservative_verdict() -> Dict[str, Any]:
    """Return a fail-closed conservative verdict."""
    return {
        "urgency": True,
        "threat": False,
        "sensitive_request": True,
        "explanation": "System error — conservative block applied"
    }
