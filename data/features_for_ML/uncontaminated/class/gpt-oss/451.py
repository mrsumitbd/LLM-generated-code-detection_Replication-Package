import base64
from typing import Any, Dict, Optional

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

    def __init__(self, provider: Any):
        """
        :param provider: An OAuthAuthorizationServerProvider instance that
                         provides access to client information.
        """
        self.provider = provider

    def _extract_credentials(self, request: Any) -> Dict[str, Optional[str]]:
        """
        Extract client_id and client_secret from the request.
        Supports Basic auth header or form parameters.
        """
        client_id: Optional[str] = None
        client_secret: Optional[str] = None

        # 1. Try Basic Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.lower().startswith("basic "):
            b64_token = auth_header.split(" ", 1)[1].strip()
            try:
                decoded = base64.b64decode(b64_token).decode("utf-8")
                client_id, client_secret = decoded.split(":", 1)
            except Exception:
                raise ValueError("Invalid Basic Authorization header")

        # 2. Fallback to form data
        if client_id is None:
            # request.form may be a dict or a callable returning a dict
            form = None
            if isinstance(request, dict):
                form = request
            elif hasattr(request, "form"):
                try:
                    form = request.form
                except Exception:
                    pass
            if form is None:
                try:
                    form = request.form()
                except Exception:
                    form = None

            if isinstance(form, dict):
                client_id = form.get("client_id")
                client_secret = form.get("client_secret")

        return {"client_id": client_id, "client_secret": client_secret}

    def __call__(self, request: Any) -> bool:
        """
        Validate the client credentials in the request.
        Raises ValueError if validation fails.
        Returns True if validation succeeds.
        """
        creds = self._extract_credentials(request)
        client_id = creds.get("client_id")
        client_secret = creds.get("client_secret")

        if not client_id:
            raise ValueError("client_id is required")

        # Retrieve client information from the provider
        client = self.provider.get_client(client_id)
        if client is None:
            raise ValueError(f"Unknown client_id: {client_id}")

        # Determine if the client requires a secret
        requires_secret = getattr(client, "secret", None) is not None

        if requires_secret:
            if not client_secret:
                raise ValueError("client_secret is required for this client")
            if client_secret != client.secret:
                raise ValueError("Invalid client_secret")

        # If no secret is required, authentication is considered successful
        return True