def get_basic_auth_token(self):
    """Gets HTTP basic authentication header (string).

    :return: The token for basic HTTP authentication.
    """
    import base64
    
    if self.username is None or self.password is None:
        return None
    
    credentials = f"{self.username}:{self.password}"
    encoded = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    return f"Basic {encoded}"