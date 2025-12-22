import numpy as np
from scipy.interpolate import interp2d

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
    # Load the pickle file containing the initial guess
    with open('initial_guess.pkl', 'rb') as f:
        psi_init, x_init, y_init = pickle.load(f)

    # Create the interpolation function
    f = interp2d(x_init, y_init, psi_init, kind='linear')

    # Evaluate the interpolation function on the computational grid
    x_grid, y_grid = np.meshgrid(self.eq.x, self.eq.y)
    psi_grid = f(self.eq.x, self.eq.y)

    # Set the initial guess for the plasma flux
    self.eq.psi = psi_grid