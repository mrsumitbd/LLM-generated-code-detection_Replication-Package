from typing import NamedTuple

class Configuration(NamedTuple):
    secret_key: str

class ParsedToken(NamedTuple):
    user_id: str
    expiration: int

def verify_internal_jwt(token: str, configuration: Configuration) -> ParsedToken:
    # Implementation of token verification logic goes here
    pass