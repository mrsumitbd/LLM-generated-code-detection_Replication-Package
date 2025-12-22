from typing import Any, Tuple, Type, TypeVar

T = TypeVar('T')

class Annotated(Generic[T]):
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

    __slots__ = ('__origin__', '__extra__')

    def __new__(cls, origin: Type[T], *extra: Any) -> 'Annotated[T]':
        if len(extra) < 1:
            raise TypeError("Annotated needs at least two arguments")
        return super().__new__(cls)

    @typing._tp_cache
    def __class_getitem__(cls, params: Tuple[Type[T], ...]) -> 'Type[Annotated[T]]':
        if not isinstance(params, tuple) or len(params) < 2:
            raise TypeError("Annotated needs at least two arguments")
        origin, *extra = params
        return cls._eval_type(origin, extra)

    def __init_subclass__(cls, *args: Any, **kwargs: Any) -> None:
        raise TypeError("Annotated cannot be subclassed")

    @classmethod
    def _eval_type(cls, origin: Type[T], extra: Tuple[Any, ...]) -> 'Type[Annotated[T]]':
        return cls(origin, *extra)