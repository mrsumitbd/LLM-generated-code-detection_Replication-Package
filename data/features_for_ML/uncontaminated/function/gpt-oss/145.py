from __future__ import annotations

from typing import Any, Type

# The following imports are placeholders. Replace them with the actual imports
# from your project where `Function` and `ToolExecutionConfig` are defined.
try:
    from your_project.types import Function, ToolExecutionConfig
except Exception:
    # Fallback definitions for type checking / documentation purposes
    class Function:
        name: str
        return_type: Type[Any]

    class ToolExecutionConfig:
        output_type: Type[Any]


def _get_function_output_type(
    function: Function,
    tool_execution_config: dict[str, ToolExecutionConfig],
) -> Type[Any]:
    """
    Determine the output type for a given function based on the provided
    tool execution configuration.

    Parameters
    ----------
    function : Function
        The function object whose output type is to be determined.
    tool_execution_config : dict[str, ToolExecutionConfig]
        Mapping from function names to their execution configuration. The
        configuration may specify an explicit `output_type`.

    Returns
    -------
    type
        The type that should be used for the function's output.

    Raises
    ------
    ValueError
        If the function name is not present in the configuration and the
        function does not expose a `return_type` attribute.
    """
    # Retrieve the configuration for the function by name
    config = tool_execution_config.get(function.name)

    # If a config exists and it specifies an output type, use it
    if config is not None:
        if hasattr(config, "output_type") and config.output_type is not None:
            return config.output_type

    # Fallback: try to use the function's own return type annotation
    if hasattr(function, "return_type") and function.return_type is not None:
        return function.return_type

    # If nothing is available, raise an informative error
    raise ValueError(
        f"Unable to determine output type for function '{function.name}'. "
        "Provide an explicit output_type in the tool_execution_config or "
        "ensure the function has a return_type attribute."
    )