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
    import os
    from dotenv import load_dotenv
    
    # Reload .env file to get latest values
    load_dotenv(override=True)
    
    # Get access token and user id from .env file
    access_token = os.getenv('SIMKL_ACCESS_TOKEN')
    user_id = os.getenv('SIMKL_USER_ID')
    
    # Get client id and secret from module-level variables (injected at build)
    client_id = globals().get('CLIENT_ID')
    client_secret = globals().get('CLIENT_SECRET')
    
    return {
        'client_id': client_id,
        'client_secret': client_secret,
        'access_token': access_token,
        'user_id': user_id
    }