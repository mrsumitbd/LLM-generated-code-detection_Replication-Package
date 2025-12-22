class CapabilityContext:
    """
    Enhanced context object for capability handlers.

    This class provides capability handlers with access to authentication information,
    task data, and other contextual information needed for processing.
    """

    def __init__(self, task: Any, auth_result: AuthenticationResult | None = None):
        self._task = task
        self._auth_result = auth_result

    @property
    def user_id(self) -> str | None:
        if self._auth_result is None:
            return None
        return getattr(self._auth_result, 'user_id', None)

    @property
    def user_scopes(self) -> set[str]:
        if self._auth_result is None:
            return set()
        scopes = getattr(self._auth_result, 'scopes', None)
        if scopes is None:
            return set()
        if isinstance(scopes, set):
            return scopes
        if isinstance(scopes, (list, tuple)):
            return set(scopes)
        return set()

    @property
    def auth_metadata(self) -> dict[str, Any]:
        if self._auth_result is None:
            return {}
        metadata = getattr(self._auth_result, 'metadata', None)
        if metadata is None:
            return {}
        if isinstance(metadata, dict):
            return metadata
        return {}

    @property
    def is_authenticated(self) -> bool:
        return self._auth_result is not None

    def has_scope(self, scope: str) -> bool:
        return scope in self.user_scopes

    def requires_scopes(self, required_scopes: set[str]) -> bool:
        return required_scopes.issubset(self.user_scopes)

    def to_dict(self) -> dict[str, Any]:
        return {
            'user_id': self.user_id,
            'user_scopes': list(self.user_scopes),
            'auth_metadata': self.auth_metadata,
            'is_authenticated': self.is_authenticated,
            'task': self._task
        }