import importlib
import pkgutil
import sys
from types import ModuleType
from typing import List


def import_extensions() -> List[ModuleType]:
    """
    Import all submodules of the ``extensions`` package that is located in the same
    directory as this module.  The function returns a list of the imported module
    objects.  Any import errors are silently ignored so that a single faulty
    extension does not prevent the rest from loading.

    Returns
    -------
    List[ModuleType]
        A list of successfully imported extension modules.
    """
    extensions: List[ModuleType] = []

    # The package name is assumed to be ``extensions`` and to live in the same
    # directory as this file.
    package_name = "extensions"

    try:
        package = importlib.import_module(package_name)
    except Exception:
        # If the package cannot be imported, nothing to do.
        return extensions

    # Iterate over all modules in the package's path.
    for _, mod_name, is_pkg in pkgutil.iter_modules(package.__path__):
        full_name = f"{package_name}.{mod_name}"
        try:
            mod = importlib.import_module(full_name)
            extensions.append(mod)
        except Exception:
            # Ignore modules that fail to import; they may be optional.
            pass

    return extensions