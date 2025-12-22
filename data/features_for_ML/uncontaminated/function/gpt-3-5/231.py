def ensure_authentication() -> str:
    raise CredentialsNotFoundError("No authentication available. Please provide valid credentials.")