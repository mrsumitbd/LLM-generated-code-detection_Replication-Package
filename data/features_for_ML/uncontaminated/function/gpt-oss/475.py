import os

def get_aksk():
    """
    Retrieve Access Key (AK) and Secret Key (SK) from environment variables.
    Supports multiple common variable names. Raises RuntimeError if not found.
    """
    # Primary names
    ak = os.getenv("AK")
    sk = os.getenv("SK")

    # Fallback names
    if not ak or not sk:
        ak = os.getenv("ACCESS_KEY")
        sk = os.getenv("SECRET_KEY")

    # AWS style names
    if not ak or not sk:
        ak = os.getenv("AWS_ACCESS_KEY_ID")
        sk = os.getenv("AWS_SECRET_ACCESS_KEY")

    if not ak or not sk:
        raise RuntimeError("AK/SK not found in environment variables")

    return ak, sk