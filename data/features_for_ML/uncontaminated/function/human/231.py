from linkedin_mcp_server.config.messages import ErrorMessages, InfoMessages
from linkedin_mcp_server.config import get_config
from linkedin_mcp_server.exceptions import CredentialsNotFoundError

def ensure_authentication() -> str:
    """
    Ensure authentication is available with clear error messages.

    Returns:
        str: Valid LinkedIn session cookie

    Raises:
        CredentialsNotFoundError: If no authentication is available with clear instructions
    """
    try:
        return get_authentication()
    except CredentialsNotFoundError:
        config = get_config()

        raise CredentialsNotFoundError(
            ErrorMessages.no_cookie_found(config.is_interactive)
        )