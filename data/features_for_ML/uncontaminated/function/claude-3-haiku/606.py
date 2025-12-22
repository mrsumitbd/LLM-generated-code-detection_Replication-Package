import numpy as np

def filterset(illuminant,
              values=[0, 0, 0],
              edges=[510, 495, 605, 590],
              transitions=[10, 10, 10, 10],
              ):
    """
    Applies a set of filters to an illuminant spectrum.

    Args:
        illuminant (numpy.ndarray): The input illuminant spectrum.
        values (list, optional): The filter values. Defaults to [0, 0, 0].
        edges (list, optional): The filter edge wavelengths. Defaults to [510, 495, 605, 590].
        transitions (list, optional): The filter transition widths. Defaults to [10, 10, 10, 10].

    Returns:
        numpy.ndarray: The filtered illuminant spectrum.
    """
    filtered_illuminant = np.copy(illuminant)

    for i, (edge, transition) in enumerate(zip(edges, transitions)):
        filtered_illuminant *= 1 / (1 + np.exp(-(illuminant - edge + transition / 2) / transition))
        filtered_illuminant *= values[i]

    return filtered_illuminant