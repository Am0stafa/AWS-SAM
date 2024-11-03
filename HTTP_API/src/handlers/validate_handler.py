from typing import Dict, Any
from services.session_service import validate_session_cookie
from utils.http import create_success_response, create_error_response

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Lambda handler for /validate endpoint"""
    try:
        headers = event.get('headers', {})
        origin = headers.get('origin', 'http://localhost:3000')
        
        cookies = headers.get("cookie", "")
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
    except Exception as e:
        return create_error_response(500, str(e), origin)
