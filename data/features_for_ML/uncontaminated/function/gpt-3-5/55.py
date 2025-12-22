import numpy as np

def rotation_matrix_from_direction(direction, reference=(0, 0, 1)):
    direction = np.array(direction)
    reference = np.array(reference)
    v = np.cross(reference, direction)
    s = np.linalg.norm(v)
    c = np.dot(reference, direction)
    skew_symmetric = np.array([[0, -v[2], v[1]],
                               [v[2], 0, -v[0]],
                               [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + skew_symmetric + np.dot(skew_symmetric, skew_symmetric) * (1 - c) / (s ** 2)
    return rotation_matrix