import os
import getpass
import datetime

# Global variable to hold the current theme
THEME = None

def set_theme():
    """
    Determine and set the application theme based on the current user,
    environment variables, and optional bypass modes.

    The logic is as follows:
    1. Retrieve the current username.
    2. If the username is in the bypass list, force the theme to 'dark'.
    3. Otherwise, check the APP_THEME environment variable:
       - If set to 'dark' or 'light', use that value.
       - If set to 'auto', choose 'dark' after 6 PM and 'light' otherwise.
    4. If no environment variable is set, default to 'light'.
    """
    global THEME

    # 1. Get the current username
    try:
        username = getpass.getuser()
    except Exception:
        username = os.getenv("USER", "default")

    # 2. Bypass list for forcing dark theme
    bypass_users = {"root", "admin", "superuser"}
    if username in bypass_users:
        THEME = "dark"
        return

    # 3. Check environment variable for theme preference
    env_theme = os.getenv("APP_THEME", "").lower()
    if env_theme in {"dark", "light"}:
        THEME = env_theme
    elif env_theme == "auto":
        # Use system time to decide
        hour = datetime.datetime.now().hour
        THEME = "dark" if hour >= 18 or hour < 6 else "light"
    else:
        # 4. Default theme
        THEME = "light"