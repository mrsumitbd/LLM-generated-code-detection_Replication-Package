from typing import TYPE_CHECKING
import utils3d

def quaternion_to_axis_angle(*args, **kwargs):
    if TYPE_CHECKING:  # redirected to:
        None, utils3d.torch.quaternion_to_axis_angle
    return _call_based_on_args('quaternion_to_axis_angle', args, kwargs)