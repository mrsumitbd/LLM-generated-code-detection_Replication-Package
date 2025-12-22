import os

def _default_session_api_keys():
    # Legacy fallback for compability with old runtime API
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        return {'api_key': api_key}
    else:
        return {}