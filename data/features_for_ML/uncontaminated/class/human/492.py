from collections.abc import Callable

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

    axes: list[int]
    symmetry_handler: Callable