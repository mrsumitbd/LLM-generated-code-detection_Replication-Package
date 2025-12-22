import numpy as np

def create_fisheye_camera(params, w, h):
    """
    Create a fisheye camera mapping.

    Parameters
    ----------
    params : dict
        Dictionary containing camera intrinsics and distortion coefficients.
        Expected keys:
            - 'f'   : focal length (scalar)
            - 'cx'  : principal point x-coordinate (scalar)
            - 'cy'  : principal point y-coordinate (scalar)
            - 'k1'  : first radial distortion coefficient (scalar)
            - 'k2'  : second radial distortion coefficient (scalar)
            - 'k3'  : third radial distortion coefficient (scalar)
            - 'k4'  : fourth radial distortion coefficient (scalar)
    w : int
        Image width in pixels.
    h : int
        Image height in pixels.

    Returns
    -------
    uv_map : ndarray
        Array of shape (h, w, 2) containing the distorted normalized
        coordinates (u, v) for each pixel.
    """
    # Extract parameters with defaults
    f   = params.get('f', 1.0)
    cx  = params.get('cx', w / 2.0)
    cy  = params.get('cy', h / 2.0)
    k1  = params.get('k1', 0.0)
    k2  = params.get('k2', 0.0)
    k3  = params.get('k3', 0.0)
    k4  = params.get('k4', 0.0)

    # Create pixel grid
    xs = np.arange(w)
    ys = np.arange(h)
    xv, yv = np.meshgrid(xs, ys, indexing='xy')

    # Normalized coordinates relative to principal point
    x_norm = (xv - cx) / f
    y_norm = (yv - cy) / f

    # Compute radial distance
    r = np.sqrt(x_norm**2 + y_norm**2)

    # Avoid division by zero for the center pixel
    r_safe = np.where(r == 0, 1e-12, r)

    # Radial distortion factor
    r_distorted = r * (1 + k1 * r**2 + k2 * r**4 + k3 * r**6 + k4 * r**8)

    # Apply distortion to normalized coordinates
    x_distorted = x_norm * (r_distorted / r_safe)
    y_distorted = y_norm * (r_distorted / r_safe)

    # Stack into UV map
    uv_map = np.stack((x_distorted, y_distorted), axis=-1)

    return uv_map