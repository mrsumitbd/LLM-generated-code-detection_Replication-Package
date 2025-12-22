import typing

class Annotated:
    """Add context specific metadata to a type.

    Example: Annotated[int, runtime_check.Unsigned] indicates to the
    hypothetical runtime_check module that this type is an unsigned int.
    Every other consumer of this type can ignore this metadata and treat
    this type as int.

    The first argument to Annotated must be a valid type (and will be in
    the __origin__ field), the remaining arguments are kept as a tuple in
    the __extra__ field.

    Details:

    - It's an error to call `Annotated` with less than two arguments.
    - Nested Annotated are flattened::

        Annotated[Annotated[T, Ann1, Ann2], Ann3] == Annotated[T, Ann1, Ann2, Ann3]

    - Instantiating an annotated type is equivalent to instantiating the
      underlying type::

        Annotated[C, Ann1](5) == C(5)

    - Annotated can be used as a generic type alias::

        Optimized = Annotated[T, runtime.Optimize()]
        Optimized[int] == Annotated[int, runtime.Optimize()]

        OptimizedList = Annotated[List[T], runtime.Optimize()]
        OptimizedList[int] == Annotated[List[int], runtime.Optimize()]
    """

    def __new__(cls, *args, **kwargs):
        if len(args) < 2:
            raise TypeError("Annotated requires at least two arguments")
        origin = args[0]
        extra = args[1:]
        # Flatten nested Annotated
        if isinstance(origin, Annotated):
            origin = origin.__origin__
            extra = origin.__extra__ + extra
        obj = super().__new__(cls)
        obj.__origin__ = origin
        obj.__extra__ = tuple(extra)
        return obj

    @typing._tp_cache
    def __class_getitem__(cls, params):
        if isinstance(params, tuple):
            return cls(*params)
        return cls(params)

    def __init_subclass__(cls, *args, **kwargs):
        raise TypeError("Annotated cannot be subclassed")

    def __call__(self, *args, **kwargs):
        if not callable(self.__origin__):
            raise TypeError(f"Underlying type {self.__origin__!r} is not callable")
        return self.__origin__(*args, **kwargs)

    def __repr__(self):
        extras = ", ".join(repr(e) for e in self.__extra__)
        return f"Annotated[{self.__origin__!r}, {extras}]"

    def __eq__(self, other):
        if not isinstance(other, Annotated):
            return False
        return self.__origin__ == other.__origin__ and self.__extra__ == other.__extra__

    def __hash__(self):
        return hash((self.__origin__, self.__extra__))