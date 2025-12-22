import base64

def get_basic_auth_token(self):
    """Gets HTTP basic authentication header (string).

    :return: The token for basic HTTP authentication.
    """
    # Retrieve username and password from the instance.
    # Try common attribute names; raise an error if not found.
    username = getattr(self, "username", None)
    password = getattr(self, "password", None)

    if username is None:
        username = getattr(self, "user", None)
    if password is None:
        password = getattr(self, "pass", None)

    if username is None or password is None:
        raise ValueError("Username and password must be set on the instance")

    # Construct the Basic auth header value.
    credentials = f"{username}:{password}"
    token = base64.b64encode(credentials.encode("utf-8")).decode("ascii")
    return f"Basic {token}"