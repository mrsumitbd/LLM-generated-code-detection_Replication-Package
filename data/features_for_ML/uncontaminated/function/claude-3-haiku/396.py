def fluid_fluid_particles_potential_radius(value):
    import numpy as np

    if value <= 0:
        return 0.0
    elif value < 1.0:
        return 1.0
    else:
        return np.sqrt(value)