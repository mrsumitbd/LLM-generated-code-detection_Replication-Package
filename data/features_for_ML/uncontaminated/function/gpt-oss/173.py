from __future__ import annotations

from typing import Dict

# Import the types that are expected to exist in the surrounding codebase.
# These imports are intentionally broad to avoid breaking if the actual
# implementations differ slightly.  The function will work with any
# objects that expose the attributes used below.
try:
    from codebase import Codebase, ProgrammingLanguage, PyClass
except Exception:
    # Fallback definitions for type checking / documentation purposes.
    class Codebase:
        def get_classes(self, language: "ProgrammingLanguage") -> list["PyClass"]:
            raise NotImplementedError

    class ProgrammingLanguage:
        PYTHON = "python"

    class PyClass:
        name: str
        decorators: list[str | "Decorator"]

        def __init__(self, name: str, decorators: list[str | "Decorator"]):
            self.name = name
            self.decorators = decorators

# The decorator name we are interested in.  It can be a string or a
# decorator object with a `name` attribute.
API_DECORATOR = "api"


def _decorator_matches(decorator: str | object) -> bool:
    """
    Return True if the decorator matches the API decorator.
    Handles plain strings, objects with a `name` attribute, and
    objects that implement ``__str__``.
    """
    if isinstance(decorator, str):
        # Strip leading @ if present.
        return decorator.lstrip("@") == API_DECORATOR
    # Try to get a name attribute.
    name = getattr(decorator, "name", None)
    if name is not None:
        return name == API_DECORATOR
    # Fallback to string representation.
    return str(decorator).lstrip("@") == API_DECORATOR


def get_api_classes_by_decorator(
    codebase: Codebase,
    language: ProgrammingLanguage = ProgrammingLanguage.PYTHON,
) -> Dict[str, PyClass]:
    """
    Return a mapping from class name to the class object for all classes
    in the given codebase that are decorated with the API decorator
    (``@api``).

    Parameters
    ----------
    codebase : Codebase
        The codebase to search.
    language : ProgrammingLanguage, optional
        The programming language to filter on.  Defaults to Python.

    Returns
    -------
    dict[str, PyClass]
        Mapping from fully‑qualified class name to the class object.
    """
    api_classes: Dict[str, PyClass] = {}

    # Retrieve all classes for the specified language.
    try:
        classes = codebase.get_classes(language)
    except AttributeError:
        # If the codebase does not expose get_classes, raise a clear error.
        raise RuntimeError(
            "The provided codebase object does not support retrieving classes."
        )

    for cls in classes:
        # Skip if the class has no decorators attribute.
        if not hasattr(cls, "decorators"):
            continue

        # Ensure decorators is iterable.
        decorators = getattr(cls, "decorators")
        if decorators is None:
            continue

        # Check each decorator for a match.
        for dec in decorators:
            if _decorator_matches(dec):
                # Use the class name as the key.  If the class has a
                # fully‑qualified name attribute, prefer that.
                key = getattr(cls, "qualified_name", getattr(cls, "name", None))
                if key:
                    api_classes[key] = cls
                break

    return api_classes