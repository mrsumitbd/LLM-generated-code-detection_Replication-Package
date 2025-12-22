def locate_idx_for_cell_with_given_id(notebook_model: Notebook, cell_id: str) -> Optional[int]:
    for idx, cell in enumerate(notebook_model.cells):
        if cell.id == cell_id:
            return idx
    return None