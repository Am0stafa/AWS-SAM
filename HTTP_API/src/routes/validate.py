from typing import Dict, Any
from ..services.session_service import validate_session_cookie
from ..utils.http import create_success_response, create_error_response

def handle_validate(event: Dict[str, Any], origin: str) -> Dict[str, Any]:
    """Handle /validate endpoint"""
    cookies = event.get("headers", {}).get("cookie", "")
    if not cookies:
        return create_error_response(401, "No session cookie found", origin)

    is_valid, message = validate_session_cookie(cookies)
    
    return create_success_response(
        {
            "valid": is_valid,
            "message": message
        },
        origin
    )
