import numpy as np

def create_fisheye_camera(params, w, h):
    # Generate UV coordinates
    x, y = np.meshgrid(np.linspace(-1, 1, w), np.linspace(-1, 1, h))
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)

    # Apply fisheye distortion
    r_distorted = params[0] * r + params[1] * r**3
    x_distorted = r_distorted * np.cos(theta)
    y_distorted = r_distorted * np.sin(theta)

    # Normalize to [-1, 1] range
    u = x_distorted
    v = y_distorted

    return u, v