from typing import Dict, Any
from services.auth_service import mock_validate_jwt, generate_session_cookie
from utils.http import create_success_response, create_error_response

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Lambda handler for /auth endpoint"""
    try:
        headers = event.get('headers', {})
        origin = headers.get('origin', 'http://localhost:3000')

        query_params = event.get("queryStringParameters", {})
        user_id = query_params.get("userId")
        
        if not user_id:
            return create_error_response(400, "userId is required", origin)
        
        is_valid, validation_message = mock_validate_jwt(user_id)
        
        if not is_valid:
            return create_error_response(401, f"Invalid token: {validation_message}", origin)
        
        session_cookie = generate_session_cookie(user_id)
        
        return create_success_response(
            {
                "message": "Authentication successful",
                "authenticated": True
            },
            origin,
            session_cookie
        )
    except Exception as e:
        return create_error_response(500, str(e), origin)
