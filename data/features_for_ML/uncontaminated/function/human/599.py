import bpy
import bpy.types

def fluid_domain_set_cfl(value):
    CFL = float(value)
    bpy.context.object.modifiers["Fluid"].domain_settings.cfl_condition = CFL