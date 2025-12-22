def initialize_from_equilibrium(self):
    """
    This function loads a pickle file containing an initial guess for the plasma
    flux (and the corners of the grid points it is located on).

    Interpolation is carried out and mapped to the computational grid specified in the
    eq class.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    import os
    import pickle
    import numpy as np
    from scipy.interpolate import griddata

    # ------------------------------------------------------------------
    # 1. Locate the equilibrium pickle file
    # ------------------------------------------------------------------
    if not hasattr(self, "equilibrium_file"):
        raise AttributeError(
            "The object must have an 'equilibrium_file' attribute pointing to the pickle file."
        )
    eq_file = self.equilibrium_file
    if not os.path.exists(eq_file):
        raise FileNotFoundError(f"Equilibrium file '{eq_file}' does not exist.")

    # ------------------------------------------------------------------
    # 2. Load the pickle data
    # ------------------------------------------------------------------
    with open(eq_file, "rb") as f:
        data = pickle.load(f)

    # Expected keys in the pickle
    required_keys = {"psi", "x", "y"}
    missing = required_keys - data.keys()
    if missing:
        raise KeyError(f"Missing required keys in equilibrium pickle: {missing}")

    psi0 = np.asarray(data["psi"])
    x0 = np.asarray(data["x"])
    y0 = np.asarray(data["y"])
    corners = data.get("corners", None)

    # ------------------------------------------------------------------
    # 3. Prepare source grid for interpolation
    # ------------------------------------------------------------------
    X0, Y0 = np.meshgrid(x0, y0, indexing="ij")
    src_points = np.column_stack((X0.ravel(), Y0.ravel()))
    src_values = psi0.ravel()

    # ------------------------------------------------------------------
    # 4. Prepare target grid from the computational eq class
    # ------------------------------------------------------------------
    if not hasattr(self, "eq"):
        raise AttributeError("The object must have an 'eq' attribute with grid information.")
    if not hasattr(self.eq, "x") or not hasattr(self.eq, "y"):
        raise AttributeError("The 'eq' object must have 'x' and 'y' attributes defining the grid.")

    Xt, Yt = np.meshgrid(self.eq.x, self.eq.y, indexing="ij")
    tgt_points = np.column_stack((Xt.ravel(), Yt.ravel()))

    # ------------------------------------------------------------------
    # 5. Interpolate onto the target grid
    # ------------------------------------------------------------------
    psi_interp = griddata(src_points, src_values, tgt_points, method="cubic")

    # Handle any NaNs that may arise from extrapolation by falling back to nearest
    nan_mask = np.isnan(psi_interp)
    if np.any(nan_mask):
        psi_interp[nan_mask] = griddata(
            src_points, src_values, tgt_points[nan_mask], method="nearest"
        )

    psi_interp = psi_interp.reshape(Xt.shape)

    # ------------------------------------------------------------------
    # 6. Store the interpolated flux in the eq object (and optionally in self)
    # ------------------------------------------------------------------
    self.eq.psi = psi_interp
    if corners is not None:
        self.eq.corners = corners

    # Store a reference in the current object for convenience
    self.psi = psi_interp