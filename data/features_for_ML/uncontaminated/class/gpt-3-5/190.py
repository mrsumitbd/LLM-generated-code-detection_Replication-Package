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
            raise TypeError("Annotated must be called with at least two arguments")
        origin = args[0]
        extra = args[1:]
        return origin

    @typing._tp_cache
    def __class_getitem__(cls, params):
        return cls

    def __init_subclass__(cls, *args, **kwargs):
        pass