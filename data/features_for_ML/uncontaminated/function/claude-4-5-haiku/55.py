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
    direction = np.array(direction, dtype=float)
    reference = np.array(reference, dtype=float)
    
    # Normalize vectors
    direction = direction / np.linalg.norm(direction)
    reference = reference / np.linalg.norm(reference)
    
    # Check if vectors are already aligned
    dot_product = np.dot(reference, direction)
    
    if np.isclose(dot_product, 1.0):
        # Vectors are already aligned
        return np.eye(3)
    elif np.isclose(dot_product, -1.0):
        # Vectors are opposite, need 180 degree rotation
        # Find an arbitrary perpendicular vector
        if abs(reference[0]) < 0.9:
            perpendicular = np.array([1.0, 0.0, 0.0])
        else:
            perpendicular = np.array([0.0, 1.0, 0.0])
        
        axis = np.cross(reference, perpendicular)
        axis = axis / np.linalg.norm(axis)
        
        # Rodrigues' rotation formula for 180 degrees
        K = np.array([
            [0, -axis[2], axis[1]],
            [axis[2], 0, -axis[0]],
            [-axis[1], axis[0], 0]
        ])
        rotation_matrix = np.eye(3) + 2 * K @ K
        return rotation_matrix
    else:
        # General case: use Rodrigues' rotation formula
        axis = np.cross(reference, direction)
        axis = axis / np.linalg.norm(axis)
        
        angle = np.arccos(np.clip(dot_product, -1.0, 1.0))
        
        # Rodrigues' rotation formula
        K = np.array([
            [0, -axis[2], axis[1]],
            [axis[2], 0, -axis[0]],
            [-axis[1], axis[0], 0]
        ])
        
        rotation_matrix = np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * (K @ K)
        return rotation_matrix