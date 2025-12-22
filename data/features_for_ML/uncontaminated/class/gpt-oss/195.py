class ScopeCache:
    def __init__(self):
        self._expanded_cache: dict[frozenset[str], frozenset[str]] = {}
        self._validation_cache: dict[tuple[frozenset[str], str], bool] = {}

    def get_expanded_scopes(self, user_scopes: frozenset[str]) -> frozenset[str] | None:
        return self._expanded_cache.get(user_scopes)

    def set_expanded_scopes(self, user_scopes: frozenset[str], expanded: frozenset[str]) -> None:
        self._expanded_cache[user_scopes] = expanded

    def get_validation_result(self, expanded_scopes: frozenset[str], required_scope: str) -> bool | None:
        return self._validation_cache.get((expanded_scopes, required_scope))

    def set_validation_result(self, expanded_scopes: frozenset[str], required_scope: str, result: bool) -> None:
        self._validation_cache[(expanded_scopes, required_scope)] = result