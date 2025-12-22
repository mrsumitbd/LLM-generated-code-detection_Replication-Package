import os

# Module‑level variables that are injected at build time.
# They may or may not exist; if they don't, the corresponding values will be None.
# Example (these are placeholders; actual values are injected during the build process):
# CLIENT_ID = "your_client_id"
# CLIENT_SECRET = "your_client_secret"

def get_credentials():
    """
    Retrieves the Simkl API credentials.

    Client ID/Secret are read from module-level variables (injected at build).
    Access Token and User ID are read directly from the .env file *each time* this
    function is called to ensure the latest values are used.

    Returns:
        dict: A dictionary containing 'client_id', 'client_secret',
              'access_token', and 'user_id'. Values might be None if not configured
              or if the build/init process failed.
    """
    # Helper to parse a .env file into a dictionary
    def _parse_env_file(path):
        env_vars = {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" not in line:
                        continue
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip()
        except FileNotFoundError:
            # If the .env file does not exist, return empty dict
            pass
        except Exception:
            # Any other error reading the file results in empty dict
            pass
        return env_vars

    # Determine the path to the .env file (assumed to be in the current working directory)
    env_path = os.path.join(os.getcwd(), ".env")
    env_vars = _parse_env_file(env_path)

    # Retrieve client credentials from module-level variables
    client_id = globals().get("CLIENT_ID")
    client_secret = globals().get("CLIENT_SECRET")

    # Retrieve access token and user id from the parsed .env file
    access_token = env_vars.get("ACCESS_TOKEN")
    user_id = env_vars.get("USER_ID")

    return {
        "client_id": client_id,
        "client_secret": client_secret,
        "access_token": access_token,
        "user_id": user_id,
    }