import bpy
import bpy.types

def collection_exists(col):
    if is_string(col):
        return col in bpy.data.collections
    return col.name in bpy.data.collections