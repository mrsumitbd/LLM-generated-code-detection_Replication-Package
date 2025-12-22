import jwt
from typing import Any

# The following imports are assumed to exist in the package.
# If they are defined elsewhere, adjust the import paths accordingly.
try:
    from .models import Configuration, ParsedToken
except Exception:
    # Fallback for environments where the relative import fails.
    from models import Configuration, ParsedToken


def verify_internal_jwt(token: str, configuration: Configuration) -> ParsedToken:
    """
    Verify an internal JWT using the provided configuration.

    The configuration is expected to expose the following attributes:
        - internal_jwt_secret: The secret key used to sign the token.
        - internal_jwt_algorithm: The algorithm used for signing (e.g., "HS256").
        - internal_jwt_issuer: (Optional) Expected issuer claim.
        - internal_jwt_audience: (Optional) Expected audience claim.

    The function decodes the token, verifies its signature, expiration,
    issuer, and audience. On success, a ParsedToken instance is returned
    containing the header and claims. On failure, a ValueError is raised.
    """
    if not token:
        raise ValueError("Token must not be empty")

    # Extract header for later use
    try:
        header = jwt.get_unverified_header(token)
    except jwt.PyJWTError as exc:
        raise ValueError(f"Invalid JWT header: {exc}") from exc

    # Prepare verification options
    options = {"require": ["exp", "iat"]}  # require expiration and issued-at

    # Build keyword arguments for decode
    decode_kwargs: dict[str, Any] = {
        "key": configuration.internal_jwt_secret,
        "algorithms": [configuration.internal_jwt_algorithm],
        "options": options,
    }

    # Optional issuer/audience checks
    if getattr(configuration, "internal_jwt_issuer", None):
        decode_kwargs["issuer"] = configuration.internal_jwt_issuer
    if getattr(configuration, "internal_jwt_audience", None):
        decode_kwargs["audience"] = configuration.internal_jwt_audience

    try:
        claims = jwt.decode(token, **decode_kwargs)
    except jwt.PyJWTError as exc:
        raise ValueError(f"JWT verification failed: {exc}") from exc

    # Construct and return the parsed token
    return ParsedToken(header=header, claims=claims)