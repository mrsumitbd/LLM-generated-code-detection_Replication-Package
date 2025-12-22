def get_basic_auth_token(self):
    """Gets HTTP basic authentication header (string).

    :return: The token for basic HTTP authentication.
    """
    username = self.username
    password = self.password
    if username and password:
        token = f"{username}:{password}"
        token = base64.b64encode(token.encode()).decode()
        return f"Basic {token}"
    return None