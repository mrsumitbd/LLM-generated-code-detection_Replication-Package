from ..types.label import LabelStyleEnum, Label
from ..types.na import NA
from ..lib import xloc as _xloc, yloc as _yloc, color as _color, size as _size, text as _text, font as _font

def set_yloc(id: Label, yloc: _yloc.YLoc) -> None:
    """
    Sets the y-location of the label

    :param id: Label object
    :param yloc: New y-location value
    """
    if isinstance(id, NA):
        return
    id.yloc = yloc