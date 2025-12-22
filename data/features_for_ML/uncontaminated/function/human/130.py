import bpy
import bpy.types

def get_objects(ref = None):
    objref = []
    if ref is None:
        objref = so()
    else:
        if isinstance(ref, list):
            if len(ref) > 0:
                if isinstance(ref[0], bpy.types.Object):
                    objref = ref
                elif isinstance(ref[0], str):
                    for ob_name in ref:
                        if object_exists(ob_name):
                            objref.append(bpy.data.objects[ob_name])
        elif is_string(ref):
            if object_exists(ref):
                objref.append(bpy.data.objects[ref])
        elif isinstance(ref, bpy.types.Object) :
            objref.append(ref)
    return objref