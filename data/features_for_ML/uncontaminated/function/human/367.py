from typing import TYPE_CHECKING
import utils3d

def masked_min(*args, **kwargs):
    if TYPE_CHECKING:  # redirected to:
        None, utils3d.torch.masked_min
    return _call_based_on_args('masked_min', args, kwargs)