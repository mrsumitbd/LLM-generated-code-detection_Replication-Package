import numpy as np

def getAff(x, y, H):
    """
    Apply a homography (or affine) transformation to a 2D point.

    Parameters
    ----------
    x, y : float
        Coordinates of the point to transform.
    H : array_like, shape (3, 3)
        Homography matrix. Can be a list of lists or a NumPy array.

    Returns
    -------
    tuple of float
        Transformed coordinates (x', y').

    Notes
    -----
    The function treats H as a 3x3 matrix and applies it to the homogeneous
    coordinate [x, y, 1]^T. The resulting homogeneous coordinate is then
    normalized by its third component. If the third component is zero,
    (inf, inf) is returned to indicate a point at infinity.
    """
    H = np.asarray(H, dtype=float)
    if H.shape != (3, 3):
        raise ValueError("H must be a 3x3 matrix")

    vec = np.array([x, y, 1.0], dtype=float)
    res = H @ vec
    w = res[2]
    if w == 0:
        return (float("inf"), float("inf"))
    return (res[0] / w, res[1] / w)