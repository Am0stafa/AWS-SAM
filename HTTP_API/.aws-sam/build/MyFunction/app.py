import json
from typing import Dict, Any
import time
from datetime import datetime, timedelta, timezone

def mock_validate_jwt(token: str) -> tuple[bool, str]:
    """Mock JWT validation - in real implementation, use proper JWT library"""

    if not token or len(token) < 10:
        return False, "Invalid token format"
    
    parts = token.split('.')
    if len(parts) != 3:
        return False, "Invalid JWT structure"
    
    return True, "valid"

def generate_session_cookie(user_id: str) -> str:
    """Generate a session cookie value"""
    expiry = (datetime.now(timezone.utc) + timedelta(hours=24)).strftime('%a, %d-%b-%Y %H:%M:%S GMT')
    return f"session={user_id}; HttpOnly; Secure; SameSite=None; Path=/; Expires={expiry}"

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        # Get origin from request headers
        headers = event.get('headers', {})
        origin = headers.get('origin', 'http://localhost:3000')  # Default to localhost

        # Validate that required event properties exist
        if not event.get("requestContext") or not event["requestContext"].get("http"):
            raise ValueError("Invalid event structure")

        query_params = event.get("queryStringParameters", {})
        user_id = query_params.get("userId")
        
        if not user_id:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": origin,
                    "Access-Control-Allow-Credentials": "true"
                },
                "body": json.dumps({
                    "error": "userId is required"
                }, indent=2)
            }
        
        is_valid, validation_message = mock_validate_jwt(user_id)
        
        if not is_valid:
            return {
                "statusCode": 401,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": origin,
                    "Access-Control-Allow-Credentials": "true"
                },
                "body": json.dumps({
                    "error": f"Invalid token: {validation_message}"
                }, indent=2)
            }
        
        session_cookie = generate_session_cookie(user_id)
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": origin,
                "Access-Control-Allow-Credentials": "true",
                "Set-Cookie": session_cookie
            },
            "body": json.dumps({
                "message": "Authentication successful",
                "authenticated": True
            }, indent=2)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": origin,
                "Access-Control-Allow-Credentials": "true"
            },
            "body": json.dumps({
                "error": str(e),
                "type": str(type(e).__name__)
            }, indent=2)
        }
