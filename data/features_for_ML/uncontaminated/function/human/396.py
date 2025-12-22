import bpy
import bpy.types

def fluid_fluid_particles_potential_radius(value):
    val = int(value)
    bpy.context.object.modifiers["Fluid"].domain_settings.sndparticle_potential_min_energy = val