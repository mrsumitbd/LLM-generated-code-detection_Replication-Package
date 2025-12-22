def get_blend_data():
    import bpy
    
    blend_data = bpy.data
    
    return {
        'objects': list(blend_data.objects),
        'meshes': list(blend_data.meshes),
        'materials': list(blend_data.materials),
        'textures': list(blend_data.textures),
        'images': list(blend_data.images),
        'scenes': list(blend_data.scenes),
        'collections': list(blend_data.collections),
        'armatures': list(blend_data.armatures),
        'actions': list(blend_data.actions),
        'lights': list(blend_data.lights),
        'cameras': list(blend_data.cameras),
    }