from typing import Any, Union

class CapabilityContext:
    """
    Enhanced context object for capability handlers.

    This class provides capability handlers with access to authentication information,
    task data, and other contextual information needed for processing.
    """

    def __init__(self, task: Any, auth_result: Union[AuthenticationResult, None] = None):
        self.task = task
        self.auth_result = auth_result

    @property
    def user_id(self) -> Union[str, None]:
        if self.auth_result:
            return self.auth_result.user_id
        return None

    @property
    def user_scopes(self) -> set[str]:
        if self.auth_result:
            return self.auth_result.scopes
        return set()

    @property
    def auth_metadata(self) -> dict[str, Any]:
        if self.auth_result:
            return self.auth_result.metadata
        return {}

    @property
    def is_authenticated(self) -> bool:
        return self.auth_result is not None

    def has_scope(self, scope: str) -> bool:
        return self.is_authenticated and scope in self.user_scopes

    def requires_scopes(self, required_scopes: set[str]) -> bool:
        return self.is_authenticated and required_scopes.issubset(self.user_scopes)

    def to_dict(self) -> dict[str, Any]:
        return {
            'user_id': self.user_id,
            'user_scopes': list(self.user_scopes),
            'auth_metadata': self.auth_metadata,
            'is_authenticated': self.is_authenticated
        }