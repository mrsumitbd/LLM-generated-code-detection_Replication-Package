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
        """Initialize a DeformationRule.

        Args:
            axes: List of indices indicating which strain components to consider
                for the specific crystal symmetry, following Voigt notation:
                [0=xx, 1=yy, 2=zz, 3=yz, 4=xz, 5=xy]
            symmetry_handler: Callable function that constructs the stress-strain
                relationship matrix according to the crystal symmetry.
        """
        self.axes = axes
        self.symmetry_handler = symmetry_handler

    def __repr__(self):
        """Return a string representation of the DeformationRule."""
        return (f"DeformationRule(axes={self.axes}, "
                f"symmetry_handler={self.symmetry_handler.__name__})")

    def __eq__(self, other):
        """Check equality between two DeformationRule instances."""
        if not isinstance(other, DeformationRule):
            return False
        return (self.axes == other.axes and 
                self.symmetry_handler == other.symmetry_handler)