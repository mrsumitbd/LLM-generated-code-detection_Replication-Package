import numpy as np
from typing import Callable, Iterable, List, Optional


class DeformationRule:
    """Defines rules for applying deformations based on crystal symmetry.

    This class specifies which axes to deform and how to handle symmetry
    constraints when calculating elastic properties.

    Attributes
    ----------
    axes : List[int]
        List of indices indicating which strain components to consider
        for the specific crystal symmetry, following Voigt notation:
        [0=xx, 1=yy, 2=zz, 3=yz, 4=xz, 5=xy]
    symmetry_handler : Callable[[np.ndarray, List[int]], np.ndarray]
        Callable function that constructs the stress‑strain relationship
        matrix according to the crystal symmetry.  The function receives
        the full 6×6 stiffness matrix and the list of active axes and
        must return a transformed matrix that respects the symmetry.
    """

    def __init__(
        self,
        axes: Iterable[int],
        symmetry_handler: Optional[Callable[[np.ndarray, List[int]], np.ndarray]] = None,
    ) -> None:
        self.axes: List[int] = sorted(set(int(a) for a in axes))
        if not all(0 <= a <= 5 for a in self.axes):
            raise ValueError("Axes must be integers in the range 0–5 (Voigt indices).")

        # Default symmetry handler simply returns the matrix unchanged.
        if symmetry_handler is None:

            def identity_handler(matrix: np.ndarray, _: List[int]) -> np.ndarray:
                return matrix

            self.symmetry_handler = identity_handler
        else:
            if not callable(symmetry_handler):
                raise TypeError("symmetry_handler must be callable")
            self.symmetry_handler = symmetry_handler

    # ------------------------------------------------------------------
    # Utility methods
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(axes={self.axes}, "
            f"symmetry_handler={self.symmetry_handler.__name__})"
        )

    def get_deformation_vector(self, strain_vector: Iterable[float]) -> np.ndarray:
        """Return a 6‑element strain vector with zeros for inactive axes.

        Parameters
        ----------
        strain_vector : Iterable[float]
            Strain components corresponding to the active axes in the order
            specified by ``self.axes``.

        Returns
        -------
        np.ndarray
            A 6‑element vector where components not in ``self.axes`` are zero.
        """
        strain = np.zeros(6, dtype=float)
        strain_vals = np.asarray(strain_vector, dtype=float)
        if strain_vals.size != len(self.axes):
            raise ValueError(
                f"Expected {len(self.axes)} strain components, got {strain_vals.size}"
            )
        for idx, ax in enumerate(self.axes):
            strain[ax] = strain_vals[idx]
        return strain

    def get_reduced_stiffness(self, stiffness_matrix: np.ndarray) -> np.ndarray:
        """Return the stiffness matrix reduced to the active axes.

        Parameters
        ----------
        stiffness_matrix : np.ndarray
            Full 6×6 stiffness matrix.

        Returns
        -------
        np.ndarray
            Reduced matrix of shape (len(axes), len(axes)).
        """
        if stiffness_matrix.shape != (6, 6):
            raise ValueError("Stiffness matrix must be 6×6.")
        return stiffness_matrix[np.ix_(self.axes, self.axes)]

    def apply_symmetry(self, stiffness_matrix: np.ndarray) -> np.ndarray:
        """Apply the symmetry handler to the full stiffness matrix.

        Parameters
        ----------
        stiffness_matrix : np.ndarray
            Full 6×6 stiffness matrix.

        Returns
        -------
        np.ndarray
            Transformed matrix that respects the crystal symmetry.
        """
        if stiffness_matrix.shape != (6, 6):
            raise ValueError("Stiffness matrix must be 6×6.")
        return self.symmetry_handler(stiffness_matrix, self.axes)

    # ------------------------------------------------------------------
    # Convenience methods for elastic property calculations
    # ------------------------------------------------------------------
    def get_reduced_compliance(self, compliance_matrix: np.ndarray) -> np.ndarray:
        """Return the compliance matrix reduced to the active axes.

        Parameters
        ----------
        compliance_matrix : np.ndarray
            Full 6×6 compliance matrix.

        Returns
        -------
        np.ndarray
            Reduced matrix of shape (len(axes), len(axes)).
        """
        if compliance_matrix.shape != (6, 6):
            raise ValueError("Compliance matrix must be 6×6.")
        return compliance_matrix[np.ix_(self.axes, self.axes)]

    def get_reduced_stress(self, stress_vector: Iterable[float]) -> np.ndarray:
        """Return a 6‑element stress vector with zeros for inactive axes.

        Parameters
        ----------
        stress_vector : Iterable[float]
            Stress components corresponding to the active axes in the order
            specified by ``self.axes``.

        Returns
        -------
        np.ndarray
            A 6‑element vector where components not in ``self.axes`` are zero.
        """
        stress = np.zeros(6, dtype=float)
        stress_vals = np.asarray(stress_vector, dtype=float)
        if stress_vals.size != len(self.axes):
            raise ValueError(
                f"Expected {len(self.axes)} stress components, got {stress_vals.size}"
            )
        for idx, ax in enumerate(self.axes):
            stress[ax] = stress_vals[idx]
        return stress