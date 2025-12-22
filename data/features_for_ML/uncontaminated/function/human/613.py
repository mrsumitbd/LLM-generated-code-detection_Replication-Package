from agentstack_server.configuration import Configuration, OidcProvider
from authlib.jose import JWTClaims, jwt
from uuid import UUID
from agentstack_server.domain.models.permissions import Permissions

def verify_internal_jwt(token: str, configuration: Configuration) -> ParsedToken:
    assert configuration.auth.jwt_secret_key
    secret_key = configuration.auth.jwt_secret_key.get_secret_value()
    payload = jwt.decode(
        token,
        key=secret_key,
        claims_options={
            "sub": {"essential": True},
            "exp": {"essential": True},
            "iss": {"essential": True, "value": "agentstack-server"},
            "aud": {"essential": True, "value": "agentstack-server"},
        },
    )
    context_id = UUID(payload["resource"][0].replace("context:", ""))
    return ParsedToken(
        global_permissions=Permissions.model_validate(payload["scope"]["global"]),
        context_permissions=Permissions.model_validate(payload["scope"]["context"]),
        context_id=context_id,
        user_id=UUID(payload["sub"]),
        raw=payload,
    )