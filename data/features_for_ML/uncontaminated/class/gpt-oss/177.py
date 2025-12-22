class DataParserFactory:
    _registry = {}

    @classmethod
    def register_loader(cls, format_name: str):
        """
        Decorator to register a loader class for a given format name.
        """
        def decorator(loader_cls):
            if not isinstance(format_name, str) or not format_name:
                raise ValueError("format_name must be a non-empty string")
            if format_name in cls._registry:
                raise KeyError(f"Loader for format '{format_name}' is already registered")
            cls._registry[format_name] = loader_cls
            return loader_cls
        return decorator

    @classmethod
    def get_loader(cls, format_name: str, **kwargs) -> object:
        """
        Instantiate and return a loader for the given format name.
        """
        if format_name not in cls._registry:
            raise KeyError(f"No loader registered for format '{format_name}'")
        loader_cls = cls._registry[format_name]
        return loader_cls(**kwargs)