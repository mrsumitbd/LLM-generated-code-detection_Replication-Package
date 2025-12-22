class DataParserFactory:
    _loaders = {}

    @classmethod
    def register_loader(cls, format_name: str):
        def decorator(loader_class):
            cls._loaders[format_name] = loader_class
            return loader_class
        return decorator

    @classmethod
    def get_loader(cls, format_name: str, **kwargs) -> object:
        if format_name not in cls._loaders:
            raise ValueError(f"No loader registered for format: {format_name}")
        return cls._loaders[format_name](**kwargs)