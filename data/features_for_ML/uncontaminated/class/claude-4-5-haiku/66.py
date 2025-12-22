class BackwardCompatibilityAdapter:
    """
    Provides backward compatibility for older MCP protocol versions.
    """

    def __init__(self, protocol_version: str):
        self.protocol_version = protocol_version
        self.version_adapters = {
            "2024-12-01": self._adapt_2024_12_01,
        }

    def adapt_request(self, method: str, params: Dict[str, Any]) -> tuple[str, Dict[str, Any]]:
        if self.protocol_version in self.version_adapters:
            adapted_method, adapted_params = self.version_adapters[self.protocol_version](
                method, params, is_request=True
            )
            return adapted_method, adapted_params
        return method, params

    def adapt_response(self, method: str, result: Any) -> Any:
        if self.protocol_version in self.version_adapters:
            _, adapted_result = self.version_adapters[self.protocol_version](
                method, result, is_request=False
            )
            return adapted_result
        return result

    def _adapt_2024_12_01(self, method: str, data: Any, is_request: bool) -> tuple[str, Any]:
        adapted_method = method
        adapted_data = data

        if is_request:
            if method == "tools/call" and isinstance(data, dict):
                if "toolName" in data:
                    data = {**data, "name": data.pop("toolName")}
                if "toolUseId" in data:
                    data = {**data, "id": data.pop("toolUseId")}
                adapted_data = data

            elif method == "resources/read" and isinstance(data, dict):
                if "resourceUri" in data:
                    data = {**data, "uri": data.pop("resourceUri")}
                adapted_data = data

            elif method == "prompts/get" and isinstance(data, dict):
                if "promptName" in data:
                    data = {**data, "name": data.pop("promptName")}
                adapted_data = data

        else:
            if method == "tools/call" and isinstance(data, dict):
                if "name" in data:
                    data = {**data, "toolName": data.pop("name")}
                if "id" in data:
                    data = {**data, "toolUseId": data.pop("id")}
                adapted_data = data

            elif method == "resources/read" and isinstance(data, dict):
                if "uri" in data:
                    data = {**data, "resourceUri": data.pop("uri")}
                adapted_data = data

            elif method == "prompts/get" and isinstance(data, dict):
                if "name" in data:
                    data = {**data, "promptName": data.pop("name")}
                adapted_data = data

        return adapted_method, adapted_data