from typing import Dict, Any, Optional, List, Set

class BackwardCompatibilityAdapter:
    """
    Provides backward compatibility for older MCP protocol versions.
    """
    
    def __init__(self, protocol_version: str):
        """
        Initialize adapter for specific protocol version.
        
        Args:
            protocol_version: Target protocol version
        """
        self.protocol_version = protocol_version
        self._adapters = {
            "2024-12-01": self._adapt_2024_12_01,
            # Add more version adapters as needed
        }
    
    def adapt_request(self, method: str, params: Dict[str, Any]) -> tuple[str, Dict[str, Any]]:
        """
        Adapt a request for backward compatibility.
        
        Args:
            method: Request method
            params: Request parameters
            
        Returns:
            Adapted (method, params)
        """
        adapter = self._adapters.get(self.protocol_version)
        if adapter:
            return adapter(method, params, is_request=True)
        return method, params
    
    def adapt_response(self, method: str, result: Any) -> Any:
        """
        Adapt a response for backward compatibility.
        
        Args:
            method: Request method that generated this response
            result: Response result
            
        Returns:
            Adapted result
        """
        adapter = self._adapters.get(self.protocol_version)
        if adapter:
            _, adapted = adapter(method, result, is_request=False)
            return adapted
        return result
    
    def _adapt_2024_12_01(self, method: str, data: Any, is_request: bool) -> tuple[str, Any]:
        """Adapter for 2024-12-01 protocol version."""
        # Example adaptations for older protocol
        
        if is_request:
            # Adapt requests to older format
            if method == "tools/list":
                # Older version might not support pagination
                if isinstance(data, dict) and "cursor" in data:
                    data = {}  # Remove pagination
            
            elif method == "prompts/list":
                # Prompts might be called something else in older version
                method = "templates/list"
        
        else:
            # Adapt responses from older format
            if method == "initialize":
                # Ensure capabilities have expected structure
                if isinstance(data, dict) and "capabilities" in data:
                    caps = data["capabilities"]
                    # Older version might not have all capability fields
                    if "logging" not in caps:
                        caps["logging"] = None
        
        return method, data