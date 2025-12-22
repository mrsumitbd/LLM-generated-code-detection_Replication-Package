from typing import Any

class JwtPayload:
    """
    Represents the payload (claims) of a JSON Web Token for APIM testing.
    https://datatracker.ietf.org/doc/html/rfc7519
    """

    def __init__(self, subject: str, name: str, issued_at: int | None = None, expires: int | None = None, roles: dict[str] | None = None) -> None:
        self.subject = subject
        self.name = name
        self.issued_at = issued_at
        self.expires = expires
        self.roles = roles

    def to_dict(self) -> dict[str, Any]:
        payload_dict = {
            'sub': self.subject,
            'name': self.name
        }
        if self.issued_at is not None:
            payload_dict['iat'] = self.issued_at
        if self.expires is not None:
            payload_dict['exp'] = self.expires
        if self.roles is not None:
            payload_dict['roles'] = self.roles
        return payload_dict