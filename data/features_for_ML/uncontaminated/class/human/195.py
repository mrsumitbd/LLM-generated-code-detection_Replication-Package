
class ScopeCache:
    def __init__(self):
        self._expanded_scopes_cache: dict[frozenset[str], frozenset[str]] = {}
        self._validation_cache: dict[tuple[frozenset[str], str], bool] = {}

    def get_expanded_scopes(self, user_scopes: frozenset[str]) -> frozenset[str] | None:
        return self._expanded_scopes_cache.get(user_scopes)

    def set_expanded_scopes(self, user_scopes: frozenset[str], expanded: frozenset[str]) -> None:
        self._expanded_scopes_cache[user_scopes] = expanded

    def get_validation_result(self, expanded_scopes: frozenset[str], required_scope: str) -> bool | None:
        cache_key = (expanded_scopes, required_scope)
        return self._validation_cache.get(cache_key)

    def set_validation_result(self, expanded_scopes: frozenset[str], required_scope: str, result: bool) -> None:
        cache_key = (expanded_scopes, required_scope)
        self._validation_cache[cache_key] = result