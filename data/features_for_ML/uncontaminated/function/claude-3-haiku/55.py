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
    direction_vector = np.array(direction)
    reference_vector = np.array(reference)

    # Normalize the direction and reference vectors
    direction_vector = direction_vector / np.linalg.norm(direction_vector)
    reference_vector = reference_vector / np.linalg.norm(reference_vector)

    # Compute the rotation axis and angle
    rotation_axis = np.cross(reference_vector, direction_vector)
    rotation_angle = np.arccos(np.dot(reference_vector, direction_vector))

    # Create the rotation matrix using Rodrigues' rotation formula
    rotation_matrix = np.eye(3)
    if np.linalg.norm(rotation_axis) > 1e-6:
        rotation_axis = rotation_axis / np.linalg.norm(rotation_axis)
        rotation_matrix = (
            rotation_matrix
            + np.sin(rotation_angle) * np.array([[0, -rotation_axis[2], rotation_axis[1]],
                                                [rotation_axis[2], 0, -rotation_axis[0]],
                                                [-rotation_axis[1], rotation_axis[0], 0]])
            + (1 - np.cos(rotation_angle)) * np.outer(rotation_axis, rotation_axis)
        )

    return rotation_matrix