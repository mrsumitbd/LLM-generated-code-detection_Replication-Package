from typing import Any
from dataclasses import dataclass, field

@dataclass
class AuthenticationResult:
    user_id: str
    user_scopes: set[str]
    auth_metadata: dict[str, Any] = field(default_factory=dict)

class CapabilityContext:
    """
    Enhanced context object for capability handlers.

    This class provides capability handlers with access to authentication information,
    task data, and other contextual information needed for processing.
    """

    def __init__(self, task: Any, auth_result: AuthenticationResult | None = None):
        self.task = task
        self.auth_result = auth_result

    @property
    def user_id(self) -> str | None:
        return self.auth_result.user_id if self.auth_result else None

    @property
    def user_scopes(self) -> set[str]:
        return self.auth_result.user_scopes if self.auth_result else set()

    @property
    def auth_metadata(self) -> dict[str, Any]:
        return self.auth_result.auth_metadata if self.auth_result else {}

    @property
    def is_authenticated(self) -> bool:
        return self.auth_result is not None

    def has_scope(self, scope: str) -> bool:
        return scope in self.user_scopes

    def requires_scopes(self, required_scopes: set[str]) -> bool:
        return all(scope in self.user_scopes for scope in required_scopes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "task": self.task,
            "user_id": self.user_id,
            "user_scopes": list(self.user_scopes),
            "auth_metadata": self.auth_metadata,
            "is_authenticated": self.is_authenticated,
        }