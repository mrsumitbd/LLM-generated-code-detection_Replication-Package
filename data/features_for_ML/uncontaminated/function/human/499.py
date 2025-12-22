from typing import TYPE_CHECKING
import utils3d

def compute_vertex_normal(*args, **kwargs):
    if TYPE_CHECKING:  # redirected to:
        utils3d.numpy.compute_vertex_normal, utils3d.torch.compute_vertex_normal
    return _call_based_on_args('compute_vertex_normal', args, kwargs)