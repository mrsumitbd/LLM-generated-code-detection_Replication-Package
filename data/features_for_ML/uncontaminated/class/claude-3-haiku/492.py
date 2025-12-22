class DeformationRule:
    """Defines rules for applying deformations based on crystal symmetry.

    This class specifies which axes to deform and how to handle symmetry
    constraints when calculating elastic properties.

    Attributes:
        axes: List of indices indicating which strain components to consider
            for the specific crystal symmetry, following Voigt notation:
            [0=xx, 1=yy, 2=zz, 3=yz, 4=xz, 5=xy]
        symmetry_handler: Callable function that constructs the stress-strain
            relationship matrix according to the crystal symmetry.
    """

    def __init__(self, axes, symmetry_handler):
        self.axes = axes
        self.symmetry_handler = symmetry_handler

    def apply_deformation(self, strain_tensor):
        """Apply the deformation rule to the given strain tensor.

        Args:
            strain_tensor (numpy.ndarray): 3x3 strain tensor.

        Returns:
            numpy.ndarray: Deformed strain tensor.
        """
        deformed_strain = strain_tensor.copy()
        for i, axis in enumerate(self.axes):
            deformed_strain[axis // 3, axis % 3] = strain_tensor[i]
        return deformed_strain

    def get_stiffness_matrix(self, elastic_constants):
        """Construct the stiffness matrix based on the crystal symmetry.

        Args:
            elastic_constants (numpy.ndarray): 6x6 matrix of elastic constants.

        Returns:
            numpy.ndarray: 6x6 stiffness matrix.
        """
        return self.symmetry_handler(elastic_constants)