import numpy as np
from enum import Enum

class ChannelDimension(Enum):
    HW = 1
    HWC = 2

def crop(
    img: np.ndarray,
    left: int,
    top: int,
    right: int,
    bottom: int,
    input_data_format: ChannelDimension,
) -> np.ndarray:
    if input_data_format == ChannelDimension.HW:
        return img[top:bottom, left:right]
    elif input_data_format == ChannelDimension.HWC:
        return img[top:bottom, left:right, :]