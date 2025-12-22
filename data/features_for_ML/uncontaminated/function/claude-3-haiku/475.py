import os
import json

def get_aksk():
    """
    Retrieves the access key and secret key from environment variables.

    Returns:
        tuple: A tuple containing the access key and secret key.
    """
    access_key = os.getenv("ACCESS_KEY")
    secret_key = os.getenv("SECRET_KEY")

    if access_key is None or secret_key is None:
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
            access_key = config["access_key"]
            secret_key = config["secret_key"]
        except (FileNotFoundError, KeyError, json.JSONDecodeError):
            raise ValueError("Access key and secret key not found in environment variables or config.json file.")

    return access_key, secret_key