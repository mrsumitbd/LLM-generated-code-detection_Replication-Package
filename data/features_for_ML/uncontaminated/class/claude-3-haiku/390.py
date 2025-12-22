from typing import Any, Optional, Dict

class JwtPayload:
    """
    Represents the payload (claims) of a JSON Web Token for APIM testing.
    https://datatracker.ietf.org/doc/html/rfc7519
    """

    def __init__(self, subject: str, name: str, issued_at: Optional[int] = None, expires: Optional[int] = None, roles: Optional[Dict[str, Any]] = None) -> None:
        self.subject = subject
        self.name = name
        self.issued_at = issued_at
        self.expires = expires
        self.roles = roles or {}

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "sub": self.subject,
            "name": self.name,
        }

        if self.issued_at is not None:
            payload["iat"] = self.issued_at

        if self.expires is not None:
            payload["exp"] = self.expires

        if self.roles:
            payload["roles"] = self.roles

        return payload