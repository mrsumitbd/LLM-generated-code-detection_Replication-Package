from typing import TYPE_CHECKING
import utils3d

def chessboard(*args, **kwargs):
    if TYPE_CHECKING:  # redirected to:
        utils3d.numpy.chessboard, utils3d.torch.chessboard
    return _call_based_on_args('chessboard', args, kwargs)