def set_yloc(id: Label, yloc: _yloc.YLoc) -> None:
    """
    Sets the y-location of the label

    :param id: Label object
    :param yloc: New y-location value
    """
    # Assign the new y-location to the label.  The Label class is expected to
    # expose a public attribute named `yloc` (or similar) that stores the
    # vertical position of the label.  If the attribute name differs, this
    # function can be adapted accordingly.
    id.yloc = yloc