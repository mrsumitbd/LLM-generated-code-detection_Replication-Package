import os
from pathlib import Path
from typing import Optional


class CredentialsNotFoundError(RuntimeError):
    """Raised when LinkedIn authentication credentials cannot be found."""


def _load_cookie_from_file(file_path: Path) -> Optional[str]:
    """Return the cookie string from a file, or None if file is missing or empty."""
    if not file_path.is_file():
        return None
    content = file_path.read_text(encoding="utf-8").strip()
    return content or None


def ensure_authentication() -> str:
    """
    Ensure authentication is available with clear error messages.

    Returns:
        str: Valid LinkedIn session cookie

    Raises:
        CredentialsNotFoundError: If no authentication is available with clear instructions
    """
    # 1. Check environment variable
    env_var = "LINKEDIN_SESSION_COOKIE"
    cookie = os.getenv(env_var)
    if cookie:
        return cookie.strip()

    # 2. Check environment variable pointing to a cookie file
    file_env_var = "LINKEDIN_COOKIE_FILE"
    file_path_str = os.getenv(file_env_var)
    if file_path_str:
        file_path = Path(file_path_str).expanduser()
        cookie = _load_cookie_from_file(file_path)
        if cookie:
            return cookie

    # 3. Check default file location (~/.linkedin_cookie)
    default_file = Path.home() / ".linkedin_cookie"
    cookie = _load_cookie_from_file(default_file)
    if cookie:
        return cookie

    # 4. No credentials found – raise an informative error
    msg_lines = [
        "LinkedIn authentication credentials not found.",
        "",
        "Please provide a valid session cookie in one of the following ways:",
        "",
        "  1. Set the environment variable 'LINKEDIN_SESSION_COOKIE' to the cookie string.",
        "  2. Create a file containing the cookie and set the environment variable",
        "     'LINKEDIN_COOKIE_FILE' to its path.",
        "  3. Place the cookie in the default file '~/.linkedin_cookie'.",
        "",
        "Example:",
        "",
        "  export LINKEDIN_SESSION_COOKIE='your_cookie_here'",
        "",
        "or",
        "",
        "  echo 'your_cookie_here' > ~/.linkedin_cookie",
        "",
        "If you are using a Docker container, you can pass the cookie via the",
        "environment variable or mount the cookie file into the container.",
    ]
    raise CredentialsNotFoundError("\n".join(msg_lines))