def set_origin_to_geometry(ref=None):
    if ref is None:
        return None
    ref_origin = ref.bounding_box.center
    ref_origin_matrix = ref.matrix_world @ ref_origin
    ref.matrix_world.translation -= ref_origin_matrix
    return ref