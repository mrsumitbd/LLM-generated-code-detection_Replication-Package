import numpy as np

def rotation_matrix_from_direction(
    direction: tuple[float, float, float],
    reference: tuple[float, float, float] = (0, 0, 1),
) -> np.ndarray:
    """Compute a rotation matrix that aligns the reference vector with the direction vector.

    Args:
        direction: The direction vector to align.
        reference: The reference vector to align with.

    Returns:
        A rotation matrix that aligns the reference vector with the direction vector.
    """
    # Convert to numpy arrays and normalize
    v = np.asarray(direction, dtype=float)
    u = np.asarray(reference, dtype=float)
    v_norm = np.linalg.norm(v)
    u_norm = np.linalg.norm(u)
    if v_norm == 0 or u_norm == 0:
        raise ValueError("Input vectors must be non-zero.")
    v = v / v_norm
    u = u / u_norm

    # Compute cross product and dot product
    axis = np.cross(u, v)
    axis_norm = np.linalg.norm(axis)
    dot = np.dot(u, v)

    # Handle special cases
    if axis_norm < 1e-12:
        # Vectors are parallel or anti-parallel
        if dot > 0:
            # Same direction: identity
            return np.eye(3)
        else:
            # Opposite direction: 180° rotation around any perpendicular axis
            # Find a vector orthogonal to u
            if abs(u[0]) < abs(u[1]):
                if abs(u[0]) < abs(u[2]):
                    ortho = np.array([1.0, 0.0, 0.0])
                else:
                    ortho = np.array([0.0, 1.0, 0.0])
            else:
                if abs(u[1]) < abs(u[2]):
                    ortho = np.array([0.0, 1.0, 0.0])
                else:
                    ortho = np.array([1.0, 0.0, 0.0])
            axis = np.cross(u, ortho)
            axis = axis / np.linalg.norm(axis)
            angle = np.pi
    else:
        axis = axis / axis_norm
        angle = np.arccos(np.clip(dot, -1.0, 1.0))

    # Rodrigues' rotation formula
    K = np.array([[0, -axis[2], axis[1]],
                  [axis[2], 0, -axis[0]],
                  [-axis[1], axis[0], 0]], dtype=float)
    R = np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * (K @ K)
    return R