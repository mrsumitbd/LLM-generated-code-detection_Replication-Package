from argparse import Namespace
from typing import Any


def _do_start_resource(args: Namespace, verbose: bool = True) -> bool:
    """
    Attempt to start a resource described by ``args``.
    The function is intentionally generic: it looks for a ``resource_name`` or ``name`` attribute
    in ``args`` and optionally calls a ``start_func`` attribute if present.
    It returns ``True`` on success and ``False`` on failure.
    """
    try:
        # Resolve the resource name
        name: str | None = getattr(args, "resource_name", None) or getattr(args, "name", None)
        if not name:
            if verbose:
                print("No resource name provided.")
            return False

        if verbose:
            print(f"Starting resource '{name}'...")

        # If the caller supplied a custom start function, use it
        start_func = getattr(args, "start_func", None)
        if callable(start_func):
            start_func(name)
        else:
            # Default behaviour: nothing to do (placeholder)
            pass

        if verbose:
            print(f"Resource '{name}' started successfully.")
        return True

    except Exception as exc:  # pragma: no cover
        if verbose:
            print(f"Failed to start resource: {exc}")
        return False