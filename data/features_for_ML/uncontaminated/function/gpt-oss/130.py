import inspect
import importlib
import importlib.util
import sys
from types import ModuleType
from typing import Any, Iterable, List, Union


def get_objects(ref: Any = None) -> List[Any]:
    """
    Retrieve objects from the given reference.

    Parameters
    ----------
    ref : Any, optional
        The reference from which to extract objects. The function accepts
        several types of input:

        * ``None`` – return all objects defined in the module where
          ``get_objects`` is defined.
        * ``str`` – interpreted as a module name or a file path. If it
          can be imported as a module, its attributes are returned.
          Otherwise, the file is loaded as a temporary module.
        * ``ModuleType`` – return the module's attributes.
        * ``type`` – return the class's attributes.
        * ``dict`` – return the dictionary's values.
        * ``list`` or ``tuple`` – return the iterable's elements.
        * Any other object – returned as a single-element list.

    Returns
    -------
    List[Any]
        A list of objects extracted from the reference.
    """
    # Helper to convert a module or class to a list of its attributes
    def _module_attrs(m: ModuleType) -> List[Any]:
        return [v for k, v in m.__dict__.items() if not k.startswith("__")]

    def _class_attrs(c: type) -> List[Any]:
        return [v for k, v in vars(c).items() if not k.startswith("__")]

    # Case 1: No reference – return objects from the current module
    if ref is None:
        current_module = inspect.getmodule(get_objects)
        if current_module is None:
            # Fallback: use globals of the caller
            caller_frame = inspect.stack()[1]
            current_module = inspect.getmodule(caller_frame[0])
            if current_module is None:
                current_module = sys.modules.get("__main__")
        return _module_attrs(current_module)

    # Case 2: String – try to import as module or load from file
    if isinstance(ref, str):
        # Try import by name
        try:
            mod = importlib.import_module(ref)
            return _module_attrs(mod)
        except ImportError:
            # Try loading from file path
            try:
                spec = importlib.util.spec_from_file_location("_tmp_module", ref)
                if spec and spec.loader:
                    tmp_mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(tmp_mod)
                    return _module_attrs(tmp_mod)
            except Exception:
                pass
        # If all fails, return empty list
        return []

    # Case 3: Module
    if isinstance(ref, ModuleType):
        return _module_attrs(ref)

    # Case 4: Class
    if inspect.isclass(ref):
        return _class_attrs(ref)

    # Case 5: Dictionary
    if isinstance(ref, dict):
        return list(ref.values())

    # Case 6: Iterable (list, tuple, set, etc.)
    if isinstance(ref, Iterable) and not isinstance(ref, (str, bytes)):
        return list(ref)

    # Default: return the object itself in a list
    return [ref]