def set_origin_to_geometry(ref=None):
    if ref is None:
        return None
    
    if hasattr(ref, 'origin'):
        ref.origin = (0, 0)
    
    if hasattr(ref, 'vertices'):
        for vertex in ref.vertices:
            vertex[0] -= ref.origin[0]
            vertex[1] -= ref.origin[1]
        ref.origin = (0, 0)
    
    if hasattr(ref, 'segments'):
        for segment in ref.segments:
            segment.start[0] -= ref.origin[0]
            segment.start[1] -= ref.origin[1]
            segment.end[0] -= ref.origin[0]
            segment.end[1] -= ref.origin[1]
        ref.origin = (0, 0)
    
    return ref