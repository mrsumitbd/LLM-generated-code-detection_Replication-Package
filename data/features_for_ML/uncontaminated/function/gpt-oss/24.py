from typing import Optional

def locate_idx_for_cell_with_given_id(notebook_model, cell_id: str) -> Optional[int]:
    """
    Return the index of the cell in `notebook_model.cells` that has the given `cell_id`.
    If no such cell exists, return None.

    Parameters
    ----------
    notebook_model : Notebook
        The notebook model object which should expose a `cells` attribute that is an
        iterable of cell objects. Each cell object is expected to have an `id`
        attribute (or a callable `get('id')`).
    cell_id : str
        The id of the cell to locate.

    Returns
    -------
    Optional[int]
        The zero‑based index of the matching cell, or None if not found.
    """
    if notebook_model is None:
        return None

    cells = getattr(notebook_model, "cells", None)
    if cells is None:
        return None

    for idx, cell in enumerate(cells):
        # Try attribute access first, then dict-style access
        cid = None
        if hasattr(cell, "id"):
            cid = getattr(cell, "id", None)
        elif isinstance(cell, dict):
            cid = cell.get("id")
        if cid == cell_id:
            return idx
    return None