def decorator(schema_cls: type[T]) -> type[T]:
    original_init = schema_cls.__init__
    
    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
    
    schema_cls.__init__ = new_init
    return schema_cls