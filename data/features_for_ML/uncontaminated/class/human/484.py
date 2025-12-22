from typing import Dict, Any, Callable, Optional, List

class ToolDefinition:
    """Tool definition with metadata"""
    name: str
    description: str
    handler: Callable
    schema: Dict[str, Any]