def decorator(schema_cls: type[T]) -> type[T]:
            if name not in cls._schemas:
                cls._schemas[name] = {}

            if version in cls._schemas[name]:
                logger.warning("Overriding existing schema for %s:%s", name, version)

            cls._schemas[name][version] = schema_cls
            logger.debug("Registered schema %s for %s:%s", schema_cls.__name__, name, version)

            return schema_cls