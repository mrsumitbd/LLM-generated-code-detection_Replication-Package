import numpy as np

def obv() -> float | np.ndarray[float]:
    """
    On Balance Volume.

    :return: On Balance Volume
    """
    # Fetch the necessary data (e.g., stock prices, trading volumes)
    prices = np.array([100.0, 101.0, 99.0, 102.0, 98.0])
    volumes = np.array([1000, 1200, 900, 1100, 950])

    # Calculate the On Balance Volume
    obv = np.zeros_like(prices)
    obv[0] = volumes[0]
    for i in range(1, len(prices)):
        if prices[i] > prices[i-1]:
            obv[i] = obv[i-1] + volumes[i]
        elif prices[i] < prices[i-1]:
            obv[i] = obv[i-1] - volumes[i]
        else:
            obv[i] = obv[i-1]

    return obv