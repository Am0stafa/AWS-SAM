from datetime import datetime, timezone
from typing import Tuple

def parse_cookie_date(date_str: str) -> datetime:
    """Parse cookie date string to datetime object"""
    return datetime.strptime(date_str, '%a, %d-%b-%Y %H:%M:%S GMT').replace(tzinfo=timezone.utc)

def validate_session_cookie(cookie_str: str) -> Tuple[bool, str]:
    """Validate session cookie and check expiration"""
    try:
        parts = cookie_str.split(';')
        expiry_part = next((p for p in parts if 'Expires=' in p), None)
        if not expiry_part:
            return False, "No expiry date found"
        
        expiry_str = expiry_part.split('=', 1)[1].strip()
        expiry_date = parse_cookie_date(expiry_str)
        
        if expiry_date <= datetime.now(timezone.utc):
            return False, "Session expired"
        
        return True, "Session valid"
    except Exception as e:
        return False, f"Invalid cookie format: {str(e)}"
