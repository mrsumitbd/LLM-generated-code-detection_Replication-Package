import bpy
import bpy.types

def set_origin_to_geometry(ref = None):
    objref = get_object(ref)
    if objref is not None:
        select_object(objref)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')