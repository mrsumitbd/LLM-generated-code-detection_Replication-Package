def display_as_textured(ref):
    objs = get_objects(ref)
    for obj in objs:
        obj.display_type = 'TEXTURED'