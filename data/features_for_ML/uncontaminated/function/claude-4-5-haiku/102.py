def initialize_from_equilibrium(self):
    """
    This function loads a pickle file containing an initial guess for the plasma
    flux (and the corners of the grid points it is located on).

    Interpolation is carried out and mapped to the computational grid specified in the
    eq class.

    Parameters
    ----------

    Returns
    -------

    """
    import pickle
    import numpy as np
    from scipy.interpolate import RectBivariateSpline
    
    # Load the pickle file containing initial equilibrium data
    if not hasattr(self, 'equilibrium_file') or self.equilibrium_file is None:
        raise ValueError("No equilibrium file specified")
    
    with open(self.equilibrium_file, 'rb') as f:
        eq_data = pickle.load(f)
    
    # Extract the flux and grid information from the loaded data
    if isinstance(eq_data, dict):
        flux_initial = eq_data.get('flux', eq_data.get('psi', None))
        r_corners = eq_data.get('r_corners', eq_data.get('r', None))
        z_corners = eq_data.get('z_corners', eq_data.get('z', None))
    else:
        # Assume it's a tuple or list: (flux, r_corners, z_corners)
        flux_initial, r_corners, z_corners = eq_data
    
    if flux_initial is None or r_corners is None or z_corners is None:
        raise ValueError("Invalid equilibrium file format")
    
    # Create interpolation function from the loaded grid
    interp_func = RectBivariateSpline(
        r_corners.flatten() if r_corners.ndim > 1 else r_corners,
        z_corners.flatten() if z_corners.ndim > 1 else z_corners,
        flux_initial,
        kx=min(3, len(np.unique(r_corners)) - 1),
        ky=min(3, len(np.unique(z_corners)) - 1)
    )
    
    # Get the computational grid from the eq class
    if not hasattr(self, 'eq') or self.eq is None:
        raise ValueError("No eq class specified")
    
    r_grid = self.eq.r
    z_grid = self.eq.z
    
    # Interpolate to the computational grid
    flux_interpolated = np.zeros_like(r_grid)
    for i in range(r_grid.shape[0]):
        for j in range(r_grid.shape[1]):
            flux_interpolated[i, j] = interp_func(r_grid[i, j], z_grid[i, j])[0, 0]
    
    # Assign the interpolated flux to the appropriate attribute
    if hasattr(self, 'psi'):
        self.psi = flux_interpolated
    elif hasattr(self, 'flux'):
        self.flux = flux_interpolated
    else:
        self.psi = flux_interpolated