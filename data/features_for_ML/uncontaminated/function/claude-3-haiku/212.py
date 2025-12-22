import numpy as np

def quaternion_to_axis_angle(*args, **kwargs):
    """
    Converts a quaternion to an axis-angle representation.

    Args:
        *args: A single quaternion as a 4-element sequence (w, x, y, z) or
            a 2D array of quaternions, where each row is a quaternion.
        **kwargs: Unused.

    Returns:
        A tuple of (axis, angle) where axis is a 3-element NumPy array
        representing the axis of rotation, and angle is a scalar
        representing the angle of rotation in radians.
    """
    if len(args) == 1 and isinstance(args[0], (list, tuple, np.ndarray)):
        q = np.array(args[0])
    else:
        q = np.array(args)

    if q.ndim == 1:
        q = q[np.newaxis, :]

    w, x, y, z = q[:, 0], q[:, 1], q[:, 2], q[:, 3]
    angle = 2 * np.arccos(w)
    axis = np.column_stack((x, y, z)) / np.sin(angle[:, np.newaxis] / 2)

    if q.shape[0] == 1:
        return axis[0], angle[0]
    else:
        return axis, angle