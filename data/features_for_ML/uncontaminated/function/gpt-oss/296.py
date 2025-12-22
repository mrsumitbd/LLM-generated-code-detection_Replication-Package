import bpy

def move_object_to_collection(ref, col):
    """
    Move an object to a specified collection.

    Parameters
    ----------
    ref : str or bpy.types.Object
        The object to move. Can be given as a name or an object reference.
    col : str or bpy.types.Collection
        The target collection. Can be given as a name or a collection reference.

    Raises
    ------
    ValueError
        If the object or collection cannot be found.
    """
    # Resolve object reference
    if isinstance(ref, str):
        obj = bpy.data.objects.get(ref)
        if obj is None:
            raise ValueError(f"Object '{ref}' not found.")
    elif isinstance(ref, bpy.types.Object):
        obj = ref
    else:
        raise TypeError("ref must be a string or bpy.types.Object")

    # Resolve collection reference
    if isinstance(col, str):
        collection = bpy.data.collections.get(col)
        if collection is None:
            raise ValueError(f"Collection '{col}' not found.")
    elif isinstance(col, bpy.types.Collection):
        collection = col
    else:
        raise TypeError("col must be a string or bpy.types.Collection")

    # Unlink from all other collections
    for c in list(obj.users_collection):
        if c != collection:
            c.objects.unlink(obj)

    # Link to target collection if not already linked
    if obj not in collection.objects:
        collection.objects.link(obj)