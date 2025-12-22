import numpy as np

def filterset(illuminant,
              values=[0, 0, 0],
              edges=[510, 495, 605, 590],
              transitions=[10, 10, 10, 10],
              ):
    """
    Apply a set of band‑pass filters to an illuminant spectrum.

    Parameters
    ----------
    illuminant : array_like or callable
        If array_like, it must be an Nx2 array where the first column
        contains wavelengths (in nm) and the second column contains the
        spectral power distribution.  If callable, it must accept a
        wavelength array and return the corresponding spectral values.
    values : list or array_like, optional
        Transmission scaling for each filter.  If a single value is
        supplied, it is applied to all filters.  If the length of
        ``values`` does not match the number of filters, it is
        broadcasted to match.
    edges : list or array_like, optional
        Center wavelengths (in nm) of the filters.
    transitions : list or array_like, optional
        Full width of the transition region (in nm) for each filter.
        The transition region is split equally on either side of the
        center wavelength.

    Returns
    -------
    filtered : ndarray
        An Nx2 array containing the wavelengths and the filtered
        spectral power distribution.
    """
    # Ensure inputs are numpy arrays
    edges = np.asarray(edges, dtype=float)
    transitions = np.asarray(transitions, dtype=float)

    # Determine the number of filters
    n_filters = len(edges)

    # Broadcast values to match number of filters
    values = np.asarray(values, dtype=float)
    if values.size == 1:
        values = np.full(n_filters, values[0], dtype=float)
    elif values.size != n_filters:
        raise ValueError("Length of 'values' must be 1 or equal to number of filters")

    # Prepare the illuminant
    if callable(illuminant):
        # Sample the illuminant over a reasonable wavelength range
        wl_min, wl_max = 380, 780
        wl = np.arange(wl_min, wl_max + 1, 1)
        spd = np.asarray(illuminant(wl), dtype=float)
    else:
        illuminant = np.asarray(illuminant, dtype=float)
        if illuminant.ndim != 2 or illuminant.shape[1] != 2:
            raise ValueError("Illuminant array must be Nx2 with wavelengths and SPD")
        wl = illuminant[:, 0]
        spd = illuminant[:, 1]

    # Create a transmission array initialized to ones
    transmission = np.ones_like(wl, dtype=float)

    # Build each filter and multiply into the transmission
    for center, width, scale in zip(edges, transitions, values):
        half = width / 2.0
        # Define the edges of the transition region
        left_start = center - half
        left_end   = center
        right_start = center
        right_end   = center + half

        # Linear ramp up on the left side
        left_mask = (wl >= left_start) & (wl < left_end)
        if left_mask.any():
            transmission[left_mask] *= scale * (wl[left_mask] - left_start) / (left_end - left_start)

        # Flat top in the middle
        middle_mask = (wl >= left_end) & (wl <= right_start)
        if middle_mask.any():
            transmission[middle_mask] *= scale

        # Linear ramp down on the right side
        right_mask = (wl > right_start) & (wl <= right_end)
        if right_mask.any():
            transmission[right_mask] *= scale * (right_end - wl[right_mask]) / (right_end - right_start)

    # Apply the transmission to the illuminant SPD
    filtered_spd = spd * transmission

    return np.column_stack((wl, filtered_spd))