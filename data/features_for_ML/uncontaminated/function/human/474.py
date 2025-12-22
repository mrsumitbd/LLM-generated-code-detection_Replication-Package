import bpy
import bpy.types

def create_nurbs_sphere_surface():
    bpy.ops.surface.primitive_nurbs_surface_sphere_add()
    return active_object()