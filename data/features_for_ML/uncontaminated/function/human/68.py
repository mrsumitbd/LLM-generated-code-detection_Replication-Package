import os

def _default_session_api_keys():
    # Legacy fallback for compability with old runtime API
    result = []
    session_api_key = os.getenv(SESSION_API_KEY_ENV)
    if session_api_key:
        result.append(session_api_key)
    return result