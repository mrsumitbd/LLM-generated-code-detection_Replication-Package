from __future__ import annotations
from typing import Callable, TypeVar, Any, get_type_hints, get_origin, get_args
import inspect
import re
from dataclasses import dataclass, field

P = TypeVar("P")
R = TypeVar("R")

# Minimal schema representations
@dataclass
class ParameterSchema:
    name: str
    type: str
    description: str = ""
    required: bool = True
    default: Any = field(default_factory=lambda: inspect._empty)

@dataclass
class ParametersSchema:
    parameters: dict[str, ParameterSchema]

@dataclass
class FunctionSpec:
    name: str
    description: str
    parameters: ParametersSchema

# Helper to map Python types to JSON Schema types
def _map_type(py_type: Any) -> str:
    origin = get_origin(py_type)
    if origin is not None:
        if origin is list or origin is List:
            return "array"
        if origin is dict or origin is Dict:
            return "object"
        if origin is Union:
            args = get_args(py_type)
            # Simplify: if any NoneType, treat as nullable
            if type(None) in args:
                non_none = [a for a in args if a is not type(None)]
                if non_none:
                    return _map_type(non_none[0])
            return "string"
    if py_type is int:
        return "integer"
    if py_type is float:
        return "number"
    if py_type is str:
        return "string"
    if py_type is bool:
        return "boolean"
    if py_type is list:
        return "array"
    if py_type is dict:
        return "object"
    return "string"

# Parse docstring for parameter descriptions
def _parse_docstring(doc: str) -> dict[str, str]:
    param_desc = {}
    if not doc:
        return param_desc
    lines = doc.splitlines()
    # Find the "Args:" section
    args_section = False
    for line in lines:
        stripped = line.strip()
        if stripped.lower().startswith("args:"):
            args_section = True
            continue
        if args_section:
            if not stripped:
                break
            # Match pattern: param_name (type, optional): description
            m = re.match(r"(\w+)\s*(?:\([^\)]*\))?:\s*(.*)", stripped)
            if m:
                name, desc = m.group(1), m.group(2)
                param_desc[name] = desc
    return param_desc

def llm_function(func: Callable[P, R]) -> Callable[P, R]:
    """
    Decorator to expose a method to the LLM (Language Learning Model) by capturing and storing its metadata.
    """
    sig = inspect.signature(func)
    hints = get_type_hints(func)
    doc = inspect.getdoc(func) or ""
    summary = doc.split("\n")[0] if doc else ""

    param_descs = _parse_docstring(doc)

    parameters = {}
    for name, param in sig.parameters.items():
        # Skip *args and **kwargs
        if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
            continue
        py_type = hints.get(name, Any)
        json_type = _map_type(py_type)
        description = param_descs.get(name, "")
        required = param.default is inspect._empty
        default = param.default if not required else inspect._empty
        parameters[name] = ParameterSchema(
            name=name,
            type=json_type,
            description=description,
            required=required,
            default=default,
        )

    func._function_spec = FunctionSpec(
        name=func.__name__,
        description=summary,
        parameters=ParametersSchema(parameters=parameters),
    )

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return func(*args, **kwargs)

    return wrapper