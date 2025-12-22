def getAff(x, y, H):
    """
    Calculate affinity between two points based on their distance and a bandwidth parameter H.
    Uses a Gaussian kernel (RBF kernel).
    """
    distance_squared = (x - y) ** 2
    affinity = np.exp(-distance_squared / (2 * H ** 2))
    return affinity