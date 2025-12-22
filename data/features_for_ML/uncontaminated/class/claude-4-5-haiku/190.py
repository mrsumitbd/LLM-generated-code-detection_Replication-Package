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
        raise TypeError("Cannot instantiate Annotated directly")

    @typing._tp_cache
    def __class_getitem__(cls, params):
        if not isinstance(params, tuple):
            params = (params,)
        
        if len(params) < 2:
            raise TypeError("Annotated[...] should be used with at least two arguments (a type and an annotation).")
        
        origin = params[0]
        metadata = params[1:]
        
        # Flatten nested Annotated
        if isinstance(origin, _AnnotatedAlias):
            metadata = origin.__metadata__ + metadata
            origin = origin.__origin__
        
        # Create and return the AnnotatedAlias instance
        return _AnnotatedAlias(origin, metadata)

    def __init_subclass__(cls, *args, **kwargs):
        raise TypeError("Cannot subclass Annotated")


class _AnnotatedAlias:
    """Internal class representing an Annotated type alias."""
    
    def __init__(self, origin, metadata):
        self.__origin__ = origin
        self.__metadata__ = metadata
    
    def __repr__(self):
        args = ", ".join([repr(self.__origin__)] + [repr(x) for x in self.__metadata__])
        return f"typing.Annotated[{args}]"
    
    def __reduce__(self):
        return operator.getitem, (
            Annotated,
            (self.__origin__,) + self.__metadata__
        )
    
    def __hash__(self):
        return hash((self.__origin__,) + self.__metadata__)
    
    def __eq__(self, other):
        if not isinstance(other, _AnnotatedAlias):
            return NotImplemented
        return self.__origin__ == other.__origin__ and self.__metadata__ == other.__metadata__
    
    def __call__(self, *args, **kwargs):
        return self.__origin__(*args, **kwargs)
    
    def __getattr__(self, name):
        if name in ('__origin__', '__metadata__'):
            return super().__getattribute__(name)
        return getattr(self.__origin__, name)
    
    def __instancecheck__(self, obj):
        return isinstance(obj, self.__origin__)
    
    def __subclasscheck__(self, cls):
        return issubclass(cls, self.__origin__)
    
    def __getitem__(self, params):
        if not isinstance(params, tuple):
            params = (params,)
        
        # Substitute type variables in origin
        new_origin = self.__origin__[params] if hasattr(self.__origin__, '__getitem__') else self.__origin__
        
        return _AnnotatedAlias(new_origin, self.__metadata__)