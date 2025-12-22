from typing import Any
from oauthlib.oauth2 import OAuth2Error
from authlib.integrations.starlette_client import OAuth

class ClientAuthenticator:
    def __init__(self, provider: OAuthAuthorizationServerProvider[Any, Any, Any]):
        self.provider = provider

    def __call__(self, request):
        if self.provider.client_authentication_required:
            client_id = request.get('client_id')
            client_secret = request.get('client_secret')
            if not client_id or not client_secret:
                raise OAuth2Error('Client authentication failed')
            if not self.provider.validate_client(client_id, client_secret):
                raise OAuth2Error('Invalid client credentials')