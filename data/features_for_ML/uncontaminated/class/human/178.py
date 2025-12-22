from .base import AuthenticationResult
from typing import Any
from agent.security.unified_auth import get_unified_auth_manager
from agent.security.unified_auth import get_unified_auth_manager

class CapabilityContext:
    """
    Enhanced context object for capability handlers.

    This class provides capability handlers with access to authentication information,
    task data, and other contextual information needed for processing.
    """

    def __init__(self, task: Any, auth_result: AuthenticationResult | None = None):
        """
        Initialize capability context.

        Args:
            task: The A2A task being processed
            auth_result: Authentication result for the request
        """
        self.task = task
        self.auth_result = auth_result or get_current_auth()

    @property
    def user_id(self) -> str | None:
        return self.auth_result.user_id if self.auth_result else None

    @property
    def user_scopes(self) -> set[str]:
        return self.auth_result.scopes or set() if self.auth_result else set()

    @property
    def auth_metadata(self) -> dict[str, Any]:
        return self.auth_result.metadata or {} if self.auth_result else {}

    @property
    def is_authenticated(self) -> bool:
        return self.auth_result is not None

    def has_scope(self, scope: str) -> bool:
        try:
            # Try to use the unified auth manager's scope hierarchy
            from agent.security.unified_auth import get_unified_auth_manager

            auth_manager = get_unified_auth_manager()
            if auth_manager:
                logger.info(f"Checking if user has scope '{scope}'")
                logger.debug(f"User scopes: {list(self.user_scopes)}")
                return auth_manager.validate_scope_access(list(self.user_scopes), scope)
            else:
                # Fallback to simple scope checking if no auth manager available
                return scope in self.user_scopes
        except ImportError:
            # Fallback if unified auth not available
            return scope in self.user_scopes

    def requires_scopes(self, required_scopes: set[str]) -> bool:
        try:
            # Try to use the unified auth manager's scope hierarchy
            from agent.security.unified_auth import get_unified_auth_manager

            auth_manager = get_unified_auth_manager()
            if auth_manager:
                return all(
                    auth_manager.validate_scope_access(list(self.user_scopes), scope) for scope in required_scopes
                )
            else:
                # Fallback to simple scope checking if no auth manager available
                return required_scopes.issubset(self.user_scopes)
        except ImportError:
            # Fallback if unified auth not available
            return required_scopes.issubset(self.user_scopes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": getattr(self.task, "id", None),
            "user_id": self.user_id,
            "scopes": list(self.user_scopes),
            "is_authenticated": self.is_authenticated,
        }