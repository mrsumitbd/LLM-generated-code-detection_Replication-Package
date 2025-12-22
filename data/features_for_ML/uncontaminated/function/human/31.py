import bpy

def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)