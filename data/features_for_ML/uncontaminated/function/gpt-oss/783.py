import importlib
from typing import Any, Dict, List, Callable
import ast

def evaluate_name(
    name: ast.Name,
    state: Dict[str, Any],
    static_tools: Dict[str, Callable],
    custom_tools: Dict[str, Callable],
    authorized_imports: List[str],
) -> Any:
    """
    Resolve an ast.Name node within the given evaluation context.

    Parameters
    ----------
    name : ast.Name
        The AST node representing the name to resolve.
    state : Dict[str, Any]
        Current variable bindings.
    static_tools : Dict[str, Callable]
        Built‑in tools that are always available.
    custom_tools : Dict[str, Callable]
        User‑defined tools that may be used.
    authorized_imports : List[str]
        Names of modules that are allowed to be imported on demand.

    Returns
    -------
    Any
        The resolved value.

    Raises
    ------
    NameError
        If the name cannot be resolved in any of the provided contexts.
    """
    # 1. Check local state
    if name.id in state:
        return state[name.id]

    # 2. Check static tools
    if name.id in static_tools:
        return static_tools[name.id]

    # 3. Check custom tools
    if name.id in custom_tools:
        return custom_tools[name.id]

    # 4. Check authorized imports
    if name.id in authorized_imports:
        try:
            module = importlib.import_module(name.id)
            return module
        except Exception as exc:
            raise NameError(f"Failed to import authorized module '{name.id}': {exc}") from exc

    # 5. Name not found
    raise NameError(f"name '{name.id}' is not defined")