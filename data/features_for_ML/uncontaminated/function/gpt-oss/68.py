import os

def _default_session_api_keys():
    """
    Legacy fallback for compatibility with old runtime API.

    Returns a dictionary containing the default API keys for the current
    session. The keys are read from environment variables:

    - OPENAI_API_KEY
    - OPENAI_ORGANIZATION
    - OPENAI_PROJECT

    The returned dictionary contains the keys ``api_key``, ``organization``,
    and ``project``. If an environment variable is not set, the corresponding
    value will be ``None``.
    """
    return {
        "api_key": os.getenv("OPENAI_API_KEY"),
        "organization": os.getenv("OPENAI_ORGANIZATION"),
        "project": os.getenv("OPENAI_PROJECT"),
    }