from typing import Tuple
from datetime import datetime, timedelta, timezone

def mock_validate_jwt(token: str) -> Tuple[bool, str]:
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
