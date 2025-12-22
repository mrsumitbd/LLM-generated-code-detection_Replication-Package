import os
from dotenv import load_dotenv

def get_credentials():
    """
    Retrieves the Simkl API credentials.

    Client ID/Secret are read from module-level variables (injected at build).
    Access Token and User ID are read directly from the .env file *each time* this function
    is called to ensure the latest values are used.

    Returns:
        dict: A dictionary containing 'client_id', 'client_secret',
              'access_token', and 'user_id'. Values might be None if not configured
              or if the build/init process failed.
    """
    load_dotenv()
    return {
        'client_id': os.getenv('SIMKL_CLIENT_ID'),
        'client_secret': os.getenv('SIMKL_CLIENT_SECRET'),
        'access_token': os.getenv('SIMKL_ACCESS_TOKEN'),
        'user_id': os.getenv('SIMKL_USER_ID')
    }