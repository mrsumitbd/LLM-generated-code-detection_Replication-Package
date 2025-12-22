import os
from typing import Optional
from linkedin_api import Linkedin
from linkedin_api.exceptions import CredentialsNotFoundError

def ensure_authentication() -> str:
    """
    Ensure authentication is available with clear error messages.

    Returns:
        str: Valid LinkedIn session cookie

    Raises:
        CredentialsNotFoundError: If no authentication is available with clear instructions
    """
    try:
        linkedin_username = os.environ.get("LINKEDIN_USERNAME")
        linkedin_password = os.environ.get("LINKEDIN_PASSWORD")
        if not linkedin_username or not linkedin_password:
            raise CredentialsNotFoundError("LinkedIn credentials not found. Please set the LINKEDIN_USERNAME and LINKEDIN_PASSWORD environment variables.")

        api = Linkedin(linkedin_username, linkedin_password)
        session_cookie = api.session.cookies.get_dict().get("li_at")
        if not session_cookie:
            raise CredentialsNotFoundError("Failed to authenticate with LinkedIn. Please check your credentials.")

        return session_cookie
    except CredentialsNotFoundError as e:
        raise CredentialsNotFoundError(str(e))
    except Exception as e:
        raise CredentialsNotFoundError(f"An error occurred while authenticating with LinkedIn: {str(e)}")