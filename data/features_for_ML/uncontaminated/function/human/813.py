import numpy as np

def getAff(x, y, H):
    h11 = H[0, 0]
    h12 = H[0, 1]
    h13 = H[0, 2]
    h21 = H[1, 0]
    h22 = H[1, 1]
    h23 = H[1, 2]
    h31 = H[2, 0]
    h32 = H[2, 1]
    h33 = H[2, 2]
    fxdx = (
        h11 / (h31 * x + h32 * y + h33)
        - (h11 * x + h12 * y + h13) * h31 / (h31 * x + h32 * y + h33) ** 2
    )
    fxdy = (
        h12 / (h31 * x + h32 * y + h33)
        - (h11 * x + h12 * y + h13) * h32 / (h31 * x + h32 * y + h33) ** 2
    )

    fydx = (
        h21 / (h31 * x + h32 * y + h33)
        - (h21 * x + h22 * y + h23) * h31 / (h31 * x + h32 * y + h33) ** 2
    )
    fydy = (
        h22 / (h31 * x + h32 * y + h33)
        - (h21 * x + h22 * y + h23) * h32 / (h31 * x + h32 * y + h33) ** 2
    )

    Aff = [[fxdx, fxdy], [fydx, fydy]]

    return np.asarray(Aff)