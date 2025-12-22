from .util.tools import Tool
from typing import Any, Callable, Coroutine, Dict, List, Optional, Type, Union
from .models.primitives import Message, MessageChunk, ToolDefinition, ToolParameters, ToolParameterProperty

def decorator(func: Callable[..., Any]) -> Callable:
            tool_name = name or func.__name__
            if tool_name in self._tools:
                if tool_name.startswith("tframex_"): # Allow re-registration for meta-tools
                     logger.debug(f"Re-registering MCP meta-tool: '{tool_name}'")
                else:
                    raise ValueError(f"Tool '{tool_name}' already registered.")

            parsed_params_obj = None
            if isinstance(parameters_schema, ToolParameters):
                parsed_params_obj = parameters_schema
            elif isinstance(parameters_schema, dict): 
                props = {
                    p_name: ToolParameterProperty(**p_def)
                    for p_name, p_def in parameters_schema.get("properties", {}).items()
                }
                required_list = parameters_schema.get("required")
                parsed_params_obj = ToolParameters(
                    properties=props, required=required_list if isinstance(required_list, list) else []
                )
            
            self._tools[tool_name] = Tool(
                name=tool_name,
                func=func,
                description=description,
                parameters_schema=parsed_params_obj, 
            )
            logger.debug(f"Registered tool: '{tool_name}'")
            return func