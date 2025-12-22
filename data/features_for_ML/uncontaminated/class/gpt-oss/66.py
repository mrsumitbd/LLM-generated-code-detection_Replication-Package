from typing import Any, Dict, Tuple


class BackwardCompatibilityAdapter:
    """
    Provides backward compatibility for older MCP protocol versions.
    """

    def __init__(self, protocol_version: str):
        self.protocol_version = protocol_version

    def adapt_request(self, method: str, params: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """
        Adapt an outgoing request to match the expectations of the target protocol version.
        """
        if self.protocol_version == "2024-12-01":
            return self._adapt_2024_12_01(method, params, is_request=True)
        # For newer or unknown versions, return the request unchanged
        return method, params

    def adapt_response(self, method: str, result: Any) -> Any:
        """
        Adapt an incoming response to match the expectations of the target protocol version.
        """
        if self.protocol_version == "2024-12-01":
            return self._adapt_2024_12_01(method, result, is_request=False)
        # For newer or unknown versions, return the response unchanged
        return result

    def _adapt_2024_12_01(self, method: str, data: Any, is_request: bool) -> Tuple[str, Any]:
        """
        Adapt request or response for the 2024-12-01 protocol version.
        """
        # Mapping tables for method names and parameters
        method_map = {
            "getUser": "fetchUser",
            "listUsers": "getUsers",
            "createUser": "addUser",
        }

        param_map = {
            "user_id": "id",
            "page": "page_number",
            "limit": "page_size",
        }

        if is_request:
            # Adapt method name
            new_method = method_map.get(method, method)

            # Adapt parameters
            if isinstance(data, dict):
                new_params = {
                    param_map.get(k, k): v for k, v in data.items()
                }
            else:
                new_params = data

            return new_method, new_params

        # Response adaptation: wrap the result in a payload dict
        # For specific methods we might need to rename keys
        if isinstance(data, dict):
            # Example: rename 'user' key to 'profile' for fetchUser
            if method == "fetchUser" and "user" in data:
                new_data = {"profile": data["user"]}
            else:
                new_data = data
        else:
            new_data = {"payload": data}

        return method, new_data