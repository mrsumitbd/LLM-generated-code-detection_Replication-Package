import pickle
import numpy as np
from scipy import interpolate

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

        # load the data from the pickle file
        with open(self.equilibrium_path, "rb") as f:
            data = pickle.load(f)

        # extract the data (will fail if not in this format)
        try:
            Rmin = data["Rmin"]
            Rmax = data["Rmax"]
            Zmin = data["Zmin"]
            Zmax = data["Zmax"]
            psi_plasma = data["psi_plasma"]
        except:
            raise ValueError(
                "Data in EQUILIBRIUM_PATH pickle not in correct format or missing."
            )

        # interpolate the plasma psi on the grid given in the data file
        plasma_psi_func = interpolate.RectBivariateSpline(
            np.linspace(Rmin, Rmax, psi_plasma.shape[0]),
            np.linspace(Zmin, Zmax, psi_plasma.shape[1]),
            psi_plasma,
        )

        # extract the values on the grid given in the eq object (this is the initial guess)
        self.plasma_psi = plasma_psi_func(self.R, self.Z, grid=False)

        print(
            "Initial guess for plasma flux initialised using file provided at EQUILIBRIUM_PATH."
        )