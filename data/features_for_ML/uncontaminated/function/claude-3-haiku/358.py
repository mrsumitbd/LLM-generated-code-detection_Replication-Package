def decorator(schema_cls: type[T]) -> type[T]:
    class DecoratedSchema(schema_cls):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.validate()

        def validate(self):
            errors = self.errors
            if errors:
                raise ValueError(errors)

    return DecoratedSchema