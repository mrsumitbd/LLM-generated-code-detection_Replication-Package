from typing import Any
import inspect

def describe_tool(tool: Any) -> str:
    """
    Return a human‑readable description of a LangChain BaseTool instance.
    The description includes the tool's name, description, and, if available,
    the signature of its callable (if it has a `function` attribute) and
    the schema of its arguments (if it has an `args_schema` attribute).
    """
    parts = []

    # Basic name and description
    name = getattr(tool, "name", None)
    if name:
        parts.append(f"Name: {name}")

    description = getattr(tool, "description", None)
    if description:
        parts.append(f"Description: {description}")

    # Function signature (if the tool exposes a callable)
    func = getattr(tool, "function", None)
    if func and callable(func):
        try:
            sig = inspect.signature(func)
            parts.append(f"Signature: {func.__name__}{sig}")
        except Exception:
            pass

    # Argument schema (if the tool exposes an args_schema)
    schema = getattr(tool, "args_schema", None)
    if schema:
        try:
            # Many schemas expose a `schema()` method that returns a dict
            schema_dict = schema.schema() if hasattr(schema, "schema") else dict(schema)
            parts.append(f"Argument schema: {schema_dict}")
        except Exception:
            pass

    return "\n".join(parts) if parts else "No description available."