import math
import numpy as np

def quaternion_to_axis_angle(*args, **kwargs):
    """
    Convert a quaternion to an axis-angle representation.

    Parameters
    ----------
    *args
        Either a single iterable of 4 elements (w, x, y, z) or four
        separate numbers (w, x, y, z).  The quaternion may be
        normalized or not; it will be normalized internally.

    Returns
    -------
    axis : ndarray
        A 3‑element unit vector representing the rotation axis.
    angle : float
        The rotation angle in radians, in the range [0, π].
    """
    # Parse arguments
    if len(args) == 1:
        q = np.asarray(args[0], dtype=float)
        if q.shape != (4,):
            raise ValueError("Quaternion must have 4 components.")
    elif len(args) == 4:
        q = np.asarray(args, dtype=float)
    else:
        raise TypeError("Expected 1 or 4 positional arguments for quaternion.")

    w, x, y, z = q

    # Normalize quaternion
    norm = math.sqrt(w*w + x*x + y*y + z*z)
    if norm == 0.0:
        raise ValueError("Zero quaternion provided.")
    w /= norm
    x /= norm
    y /= norm
    z /= norm

    # Compute angle
    # Clamp w to [-1, 1] to avoid numerical errors in acos
    w_clamped = max(-1.0, min(1.0, w))
    angle = 2.0 * math.acos(w_clamped)

    # Compute axis
    sin_half_angle = math.sqrt(1.0 - w_clamped*w_clamped)
    if sin_half_angle < 1e-8:
        # Angle is 0 or π; axis is arbitrary. Use default axis.
        axis = np.array([1.0, 0.0, 0.0], dtype=float)
    else:
        axis = np.array([x, y, z], dtype=float) / sin_half_angle

    return axis, angle