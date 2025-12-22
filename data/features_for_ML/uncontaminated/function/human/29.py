from typing import TYPE_CHECKING
import utils3d

def masked_max(*args, **kwargs):
    if TYPE_CHECKING:  # redirected to:
        None, utils3d.torch.masked_max
    return _call_based_on_args('masked_max', args, kwargs)