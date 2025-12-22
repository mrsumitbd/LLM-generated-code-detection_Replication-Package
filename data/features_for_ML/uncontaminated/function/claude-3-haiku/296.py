def move_object_to_collection(ref, col):
    if ref in col:
        col.remove(ref)
    col.append(ref)