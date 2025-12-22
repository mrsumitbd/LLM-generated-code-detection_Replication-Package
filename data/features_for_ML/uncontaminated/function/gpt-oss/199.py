from typing import get_args, Any

def extract_type_arg(typ: type, index: int) -> type:
    """
    Return the type argument at the given index from a generic type.

    Parameters
    ----------
    typ : type
        A generic type such as `list[int]`, `dict[str, int]`, or a typing
        construct like `typing.List[int]`.
    index : int
        Zero‑based index of the type argument to extract.

    Returns
    -------
    type
        The type argument at the requested index.

    Raises
    ------
    TypeError
        If the supplied type does not have any type arguments.
    IndexError
        If the index is out of range for the available type arguments.
    """
    args = get_args(typ)
    if not args:
        raise TypeError(f"Type {typ!r} has no type arguments")
    if index < 0 or index >= len(args):
        raise IndexError(
            f"Index {index} out of range for type arguments of {typ!r}"
        )
    return args[index]