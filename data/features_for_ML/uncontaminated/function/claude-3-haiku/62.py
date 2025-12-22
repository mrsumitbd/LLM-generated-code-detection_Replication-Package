def get_voltages(shotn):
    import numpy as np
    
    # Define the voltage values for each shot
    voltages = {
        1: np.array([100.0, 101.2, 99.8, 100.5, 100.1]),
        2: np.array([99.5, 100.0, 100.3, 99.8, 100.2]),
        3: np.array([100.2, 99.9, 100.1, 100.0, 99.7]),
        4: np.array([99.8, 100.1, 100.0, 99.9, 100.1]),
        5: np.array([100.0, 100.2, 99.9, 100.1, 100.0])
    }
    
    # Return the voltage values for the given shot number
    return voltages[shotn]