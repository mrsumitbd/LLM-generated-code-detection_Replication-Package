from typing import Dict, Any

class BackwardCompatibilityAdapter:
    """
    Provides backward compatibility for older MCP protocol versions.
    """

    def __init__(self, protocol_version: str):
        self.protocol_version = protocol_version

    def adapt_request(self, method: str, params: Dict[str, Any]) -> tuple[str, Dict[str, Any]]:
        if self.protocol_version == '2024-12-01':
            return self._adapt_2024_12_01(method, params, is_request=True)
        # Add more adapt_request implementations for other protocol versions if needed

    def adapt_response(self, method: str, result: Any) -> Any:
        if self.protocol_version == '2024-12-01':
            return self._adapt_2024_12_01(method, result, is_request=False)
        # Add more adapt_response implementations for other protocol versions if needed

    def _adapt_2024_12_01(self, method: str, data: Any, is_request: bool) -> tuple[str, Any]:
        # Implementation specific to protocol version '2024-12-01'
        if is_request:
            # Adapt request data
            adapted_data = data
        else:
            # Adapt response data
            adapted_data = data
        return method, adapted_data