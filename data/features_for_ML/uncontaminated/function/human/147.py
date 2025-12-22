from collections.abc import Callable

def wrapper(wrapped: Callable[P, T], instance: "Editable", args, kwargs) -> T:
        if instance is None:
            instance = args[0]
        if instance.removed:
            logger.warning("Editing a removed node")
        autocommit = instance.ctx._autocommit
        logger.debug("Writing node %r,%r", instance, wrapped)
        with autocommit.write_state(instance, commit=commit):
            return wrapped(*args, **kwargs)