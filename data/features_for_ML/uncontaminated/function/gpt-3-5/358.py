def decorator(schema_cls: type[T]) -> type[T]:
    class DecoratedClass(schema_cls):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Add your custom initialization code here

    return DecoratedClass