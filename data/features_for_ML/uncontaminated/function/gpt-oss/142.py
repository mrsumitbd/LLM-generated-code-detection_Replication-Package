def fluid_field_weights_gravity(value):
    """
    Compute the weight of a fluid in a gravitational field.

    Parameters
    ----------
    value : float, int, tuple/list of two floats, or dict
        * If a scalar, it is interpreted as the mass (kg) of the fluid.
          The weight is then mass * g.
        * If a tuple/list of two elements, they are interpreted as
          (density [kg/m³], volume [m³]).
        * If a dict, it must contain the keys:
            - 'density' (kg/m³)
            - 'volume'  (m³)
          Optionally it may contain:
            - 'gravity' (m/s²)
          If 'gravity' is omitted, the standard gravity 9.80665 m/s² is used.

    Returns
    -------
    float
        The weight in newtons (N).

    Raises
    ------
    TypeError
        If the input type is unsupported.
    ValueError
        If required keys are missing in a dict input.
    """
    # Standard gravity in m/s²
    g_std = 9.80665

    # Case 1: scalar mass
    if isinstance(value, (int, float)):
        return float(value) * g_std

    # Case 2: tuple or list of two elements (density, volume)
    if isinstance(value, (tuple, list)) and len(value) == 2:
        density, volume = value
        return float(density) * float(volume) * g_std

    # Case 3: dictionary with density, volume, optional gravity
    if isinstance(value, dict):
        try:
            density = float(value['density'])
            volume = float(value['volume'])
        except KeyError as e:
            raise ValueError(f"Missing required key in dict: {e}") from None
        gravity = float(value.get('gravity', g_std))
        return density * volume * gravity

    # Unsupported type
    raise TypeError(
        f"Unsupported type for fluid_field_weights_gravity: {type(value).__name__}"
    )