class ScopeCache:

    def __init__(self):
        self.cache = {}

    def get_expanded_scopes(self, user_scopes: frozenset[str]) -> frozenset[str] | None:
        return self.cache.get(user_scopes)

    def set_expanded_scopes(self, user_scopes: frozenset[str], expanded: frozenset[str]) -> None:
        self.cache[user_scopes] = expanded

    def get_validation_result(self, expanded_scopes: frozenset[str], required_scope: str) -> bool | None:
        return self.cache.get(expanded_scopes, {}).get(required_scope)

    def set_validation_result(self, expanded_scopes: frozenset[str], required_scope: str, result: bool) -> None:
        if expanded_scopes not in self.cache:
            self.cache[expanded_scopes] = {}
        self.cache[expanded_scopes][required_scope] = result