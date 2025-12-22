import jwt
from datetime import datetime, timezone
from typing import NamedTuple

class ParsedToken(NamedTuple):
    user_id: str
    exp: datetime
    iat: datetime

def verify_internal_jwt(token: str, configuration: Configuration) -> ParsedToken:
    try:
        payload = jwt.decode(token, configuration.secret_key, algorithms=[configuration.algorithm])
        user_id = payload['user_id']
        exp = datetime.fromtimestamp(payload['exp'], tz=timezone.utc)
        iat = datetime.fromtimestamp(payload['iat'], tz=timezone.utc)
        return ParsedToken(user_id, exp, iat)
    except (jwt.exceptions.InvalidTokenError, KeyError) as e:
        raise ValueError("Invalid JWT token") from e