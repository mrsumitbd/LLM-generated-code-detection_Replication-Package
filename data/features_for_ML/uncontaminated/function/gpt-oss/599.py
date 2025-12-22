def fluid_domain_set_cfl(value):
    """
    Set the CFL (Courant–Friedrichs–Lewy) number for the fluid domain.

    Parameters
    ----------
    value : float or int
        The desired CFL number. Must be a positive real number.

    Raises
    ------
    TypeError
        If `value` is not a real number.
    ValueError
        If `value` is not positive.
    """
    # Validate type
    if not isinstance(value, (int, float)):
        raise TypeError(f"CFL value must be a real number, got {type(value).__name__}")

    # Validate positivity
    if value <= 0:
        raise ValueError(f"CFL value must be positive, got {value}")

    # Store the value in a module-level variable
    global _fluid_domain_cfl
    _fluid_domain_cfl = float(value)