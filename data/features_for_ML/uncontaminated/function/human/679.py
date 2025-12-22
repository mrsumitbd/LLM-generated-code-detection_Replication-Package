from typing import TYPE_CHECKING
import utils3d

def compute_connected_components(*args, **kwargs):
    if TYPE_CHECKING:  # redirected to:
        None, utils3d.torch.compute_connected_components
    return _call_based_on_args('compute_connected_components', args, kwargs)