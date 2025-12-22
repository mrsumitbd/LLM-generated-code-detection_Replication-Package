import importlib.util
from typing import Any

class ExternalImportResolver:
    """
    Resolve an external import to the file path of the module it refers to.
    If the module cannot be found, None is returned.
    """

    def resolve(self, imp: Any) -> str | None:
        """
        Resolve the given import object to the path of the module it refers to.

        Parameters
        ----------
        imp : Any
            An object representing an import. It is expected to have a
            ``module_name`` attribute or property that contains the fully
            qualified name of the module to import.

        Returns
        -------
        str | None
            The absolute path to the module file if it can be resolved,
            otherwise None.
        """
        # Attempt to extract the module name from the import object.
        module_name = getattr(imp, "module_name", None)
        if not module_name:
            return None

        try:
            # Use importlib to locate the module specification.
            spec = importlib.util.find_spec(module_name)
            if spec and spec.origin:
                return spec.origin
        except Exception:
            # Any error (e.g., invalid module name) results in a None return.
            return None

        return None