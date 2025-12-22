from ..types.linefill import LineFill
from ..types.line import Line
from ..types.na import NA

def get_line1(id: LineFill) -> Line | NA:
    """
    Returns the ID of the first line used in the id linefill.

    :param id: A linefill object
    :return: First line object
    """
    if isinstance(id, NA):
        return NA(Line)
    return id.line1