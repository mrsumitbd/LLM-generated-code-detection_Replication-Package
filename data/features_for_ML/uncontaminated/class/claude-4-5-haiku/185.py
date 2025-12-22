class ExternalImportResolver:

    def resolve(self, imp: Import) -> str | None:
        """
        Resolve an external import to its module path.
        
        Args:
            imp: An Import object containing import information
            
        Returns:
            The resolved module path as a string, or None if resolution fails
        """
        if not imp or not hasattr(imp, 'module'):
            return None
        
        module_name = imp.module
        
        if not module_name:
            return None
        
        try:
            import importlib.util
            spec = importlib.util.find_spec(module_name)
            if spec and spec.origin:
                return spec.origin
        except (ImportError, ModuleNotFoundError, ValueError, AttributeError):
            pass
        
        return None