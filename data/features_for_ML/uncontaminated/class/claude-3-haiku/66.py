class BackwardCompatibilityAdapter:
    """
    Provides backward compatibility for older MCP protocol versions.
    """

    def __init__(self, protocol_version: str):
        self.protocol_version = protocol_version

    def adapt_request(self, method: str, params: Dict[str, Any]) -> tuple[str, Dict[str, Any]]:
        if self.protocol_version == "2024-12-01":
            return self._adapt_2024_12_01(method, params, is_request=True)
        return method, params

    def adapt_response(self, method: str, result: Any) -> Any:
        if self.protocol_version == "2024-12-01":
            _, adapted_result = self._adapt_2024_12_01(method, result, is_request=False)
            return adapted_result
        return result

    def _adapt_2024_12_01(self, method: str, data: Any, is_request: bool) -> tuple[str, Any]:
        if is_request:
            if method == "create_user":
                data["email"] = data.pop("username")
            elif method == "update_user":
                data["email"] = data.pop("username", None)
        else:
            if method == "get_user":
                data["username"] = data.pop("email")
        return method, data