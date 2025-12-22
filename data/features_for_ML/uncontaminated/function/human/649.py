import bpy

def get_blend_data():

    if '.vrt-data' not in bpy.data.texts:
        data = bpy.data.texts.new('.vrt-data')
    else:
        data = bpy.data.texts['.vrt-data']

    return data