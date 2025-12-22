class ClientAuthenticator:
    """
    ClientAuthenticator is a callable which validates requests from a client
    application, used to verify /token calls.
    If, during registration, the client requested to be issued a secret, the
    authenticator asserts that /token calls must be authenticated with
    that same token.
    NOTE: clients can opt for no authentication during registration, in which case this
    logic is skipped.
    """

    def __init__(self, provider: OAuthAuthorizationServerProvider[Any, Any, Any]):
        self.provider = provider

    def __call__(self, request: Request) -> Client:
        """
        Authenticate a client from the request.
        
        Args:
            request: The HTTP request containing client credentials
            
        Returns:
            The authenticated Client object
            
        Raises:
            InvalidClientError: If client authentication fails
        """
        client_id = self._get_client_id(request)
        client_secret = self._get_client_secret(request)
        
        client = self.provider.get_client(client_id)
        
        if client is None:
            raise InvalidClientError("Client not found")
        
        if client.requires_authentication():
            if client_secret is None:
                raise InvalidClientError("Client secret required")
            
            if not client.authenticate(client_secret):
                raise InvalidClientError("Invalid client secret")
        
        return client
    
    def _get_client_id(self, request: Request) -> str:
        """Extract client_id from request."""
        if request.method == "POST":
            client_id = request.form.get("client_id")
            if client_id:
                return client_id
        
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Basic "):
            try:
                credentials = base64.b64decode(auth_header[6:]).decode("utf-8")
                client_id, _ = credentials.split(":", 1)
                return client_id
            except (ValueError, TypeError):
                pass
        
        raise InvalidClientError("Missing client_id")
    
    def _get_client_secret(self, request: Request) -> Optional[str]:
        """Extract client_secret from request."""
        if request.method == "POST":
            client_secret = request.form.get("client_secret")
            if client_secret:
                return client_secret
        
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Basic "):
            try:
                credentials = base64.b64decode(auth_header[6:]).decode("utf-8")
                _, client_secret = credentials.split(":", 1)
                return client_secret
            except (ValueError, TypeError):
                pass
        
        return None