def getAff(x, y, H):
    import numpy as np

    # Calculate the affine transformation matrix
    A = np.array([[H[0, 0], H[0, 1], H[0, 2]],
                  [H[1, 0], H[1, 1], H[1, 2]],
                  [H[2, 0], H[2, 1], H[2, 2]]])

    # Apply the affine transformation to the input coordinates (x, y)
    transformed_coords = np.dot(A, np.array([x, y, 1]))

    # Extract the transformed x and y coordinates
    transformed_x = transformed_coords[0]
    transformed_y = transformed_coords[1]

    return transformed_x, transformed_y