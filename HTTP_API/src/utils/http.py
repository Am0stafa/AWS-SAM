from typing import Dict, Any
import json

def create_response(status_code: int, body: Dict[str, Any], origin: str) -> Dict[str, Any]:
    """Create standardized HTTP response"""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true"
        },
        "body": json.dumps(body, indent=2)
    }

def create_error_response(status_code: int, error: str, origin: str) -> Dict[str, Any]:
    """Create standardized error response"""
    return create_response(status_code, {"error": error}, origin)

def create_success_response(body: Dict[str, Any], origin: str, cookie: str = None) -> Dict[str, Any]:
    """Create standardized success response"""
    response = create_response(200, body, origin)
    if cookie:
        response["headers"]["Set-Cookie"] = cookie
    return response
