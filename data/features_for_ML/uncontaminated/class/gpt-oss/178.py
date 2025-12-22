from __future__ import annotations

from typing import Any, Optional, Set

# The AuthenticationResult type is expected to be defined elsewhere in the codebase.
# It should expose at least the following attributes:
#   - user_id: str
#   - scopes: Iterable[str]
#   - metadata: Mapping[str, Any]
# If it differs, adjust the attribute names accordingly.
try:
    from authentication import AuthenticationResult  # type: ignore
except Exception:  # pragma: no cover
    # Fallback stub for type checking / documentation purposes.
    class AuthenticationResult:  # pragma: no cover
        user_id: str
        scopes: Set[str]
        metadata: dict[str, Any]


class CapabilityContext:
    """
    Enhanced context object for capability handlers.

    This class provides capability handlers with access to authentication information,
    task data, and other contextual information needed for processing.
    """

    def __init__(self, task: Any, auth_result: Optional[AuthenticationResult] = None):
        self._task = task
        self._auth_result = auth_result

    @property
    def user_id(self) -> Optional[str]:
        """Return the authenticated user's ID, or None if not authenticated."""
        return getattr(self._auth_result, "user_id", None)

    @property
    def user_scopes(self) -> Set[str]:
        """Return a set of scopes granted to the authenticated user."""
        scopes = getattr(self._auth_result, "scopes", set())
        return set(scopes) if scopes is not None else set()

    @property
    def auth_metadata(self) -> dict[str, Any]:
        """Return any additional authentication metadata."""
        return getattr(self._auth_result, "metadata", {})

    @property
    def is_authenticated(self) -> bool:
        """Return True if an authentication result is present."""
        return self._auth_result is not None

    def has_scope(self, scope: str) -> bool:
        """Check whether the authenticated user has a specific scope."""
        return scope in self.user_scopes

    def requires_scopes(self, required_scopes: Set[str]) -> bool:
        """
        Verify that the authenticated user possesses all required scopes.

        Returns False if the user is not authenticated or if any required scope is missing.
        """
        if not self.is_authenticated:
            return False
        return required_scopes.issubset(self.user_scopes)

    def to_dict(self) -> dict[str, Any]:
        """Return a dictionary representation of the context."""
        return {
            "task": self._task,
            "user_id": self.user_id,
            "user_scopes": list(self.user_scopes),
            "auth_metadata": self.auth_metadata,
            "is_authenticated": self.is_authenticated,
        }