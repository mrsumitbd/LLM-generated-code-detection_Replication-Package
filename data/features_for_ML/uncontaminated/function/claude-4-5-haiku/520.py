def set_origin_to_geometry(ref = None):
    import bpy
    
    # Get the active object if no reference is provided
    if ref is None:
        ref = bpy.context.active_object
    
    if ref is None:
        return
    
    # Store the current cursor location
    cursor_location = bpy.context.scene.cursor.location.copy()
    
    # Set cursor to world origin
    bpy.context.scene.cursor.location = (0, 0, 0)
    
    # Set the object's origin to the 3D cursor (world origin)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
    # Restore the cursor location
    bpy.context.scene.cursor.location = cursor_location