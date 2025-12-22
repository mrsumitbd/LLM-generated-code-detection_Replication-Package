import bpy
import bpy.types

def fluid_field_weights_gravity(value):
    val = float(value)
    bpy.context.object.modifiers["Fluid"].domain_settings.effector_weights.gravity = val