from typing import Dict, Any
from routes.auth import handle_auth
from routes.validate import handle_validate
from utils.http import create_error_response

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        headers = event.get('headers', {})
        origin = headers.get('origin', 'http://localhost:3000')
        
        path = event.get("requestContext", {}).get("http", {}).get("path", "")

        if path == "/auth":
            return handle_auth(event, origin)
        elif path == "/validate":
            return handle_validate(event, origin)
        else:
            return create_error_response(404, f"Unknown path: {path}", origin)

    except Exception as e:
        return create_error_response(500, str(e), origin)
