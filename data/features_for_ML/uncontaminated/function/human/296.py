def move_object_to_collection(ref, col):
    objref = get_object(ref)
    colref = None
    if is_string(col):
        colref = get_collection(col)
    else:
        colref = col

    cols = objref.users_collection
    for c in cols:
        c.objects.unlink(objref)
    link_object_to_collection(objref, colref)