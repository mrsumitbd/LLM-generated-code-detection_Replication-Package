def ensure_authentication() -> str:
    """
    Ensure authentication is available with clear error messages.

    Returns:
        str: Valid LinkedIn session cookie

    Raises:
        CredentialsNotFoundError: If no authentication is available with clear instructions
    """
    import os
    from typing import Optional
    
    # Try to get session cookie from environment variable
    session_cookie: Optional[str] = os.getenv('LINKEDIN_SESSION_COOKIE')
    
    if session_cookie and session_cookie.strip():
        return session_cookie.strip()
    
    # If not found, raise error with clear instructions
    error_message = (
        "LinkedIn authentication credentials not found.\n"
        "Please set the LINKEDIN_SESSION_COOKIE environment variable.\n"
        "Instructions:\n"
        "1. Log in to LinkedIn in your browser\n"
        "2. Open Developer Tools (F12)\n"
        "3. Go to Application/Storage tab\n"
        "4. Find Cookies for linkedin.com\n"
        "5. Copy the 'li_a' or session cookie value\n"
        "6. Set it as: export LINKEDIN_SESSION_COOKIE='<your_cookie>'"
    )
    
    class CredentialsNotFoundError(Exception):
        pass
    
    raise CredentialsNotFoundError(error_message)