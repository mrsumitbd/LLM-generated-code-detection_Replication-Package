from dotenv import dotenv_values, load_dotenv
import os

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

    client_id = SIMKL_CLIENT_ID
    client_secret = SIMKL_CLIENT_SECRET
    
    if not client_id or not client_secret:
        logger.debug("Build-injected credentials not found, trying development sources...")
        
        client_id = os.environ.get("SIMKL_CLIENT_ID")
        client_secret = os.environ.get("SIMKL_CLIENT_SECRET")
        
        if (not client_id or not client_secret) and DEV_CREDS_PATH.exists():
            logger.debug(f"Loading development credentials from {DEV_CREDS_PATH}")
            dev_config = dotenv_values(DEV_CREDS_PATH)
            client_id = client_id or dev_config.get("SIMKL_CLIENT_ID")
            client_secret = client_secret or dev_config.get("SIMKL_CLIENT_SECRET")

 
    access_token = None
    user_id = None
    env_file_path = get_env_file_path() 
    if env_file_path.exists():
        logger.debug(f"Reading credentials from {env_file_path} inside get_credentials()")
        config = dotenv_values(env_file_path)
        access_token = config.get("SIMKL_ACCESS_TOKEN")
        user_id = config.get("SIMKL_USER_ID")
        
        if user_id:
            logger.debug(f"Found user ID in env file: {user_id}")
        else:
            logger.debug("User ID not found in env file")
            
        if not access_token:
             logger.warning(f"Found env file at {env_file_path}, but SIMKL_ACCESS_TOKEN key is missing or empty.")
    else:
         logger.debug(f"Env file not found at {env_file_path} inside get_credentials()")

    if not client_id or not client_secret:
         logger.warning("Client ID or Secret not found. For local development, create a dev_credentials.env file with SIMKL_CLIENT_ID and SIMKL_CLIENT_SECRET.")

    return {
        "client_id": client_id,
        "client_secret": client_secret,
        "access_token": access_token,
        "user_id": user_id
    }