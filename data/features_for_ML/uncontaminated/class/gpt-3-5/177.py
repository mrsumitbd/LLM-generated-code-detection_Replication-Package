class DataParserFactory:
    loaders = {}

    @classmethod
    def register_loader(cls, format_name: str):
        def decorator(loader_cls):
            cls.loaders[format_name] = loader_cls
            return loader_cls
        return decorator

    @classmethod
    def get_loader(cls, format_name: str, **kwargs) -> object:
        loader_cls = cls.loaders.get(format_name)
        if loader_cls:
            return loader_cls(**kwargs)
        else:
            raise ValueError(f"Loader for format '{format_name}' not registered")