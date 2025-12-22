import bpy
import bpy.types

def flow_initial_velocity_toggle(value):
    if value.upper() == 'FALSE':
        h =bool(False)
    elif value.upper() == 'TRUE':
        h =bool(True)
    bpy.context.object.modifiers["Fluid"].flow_settings.use_initial_velocity = h