from typing import Optional, Any, Dict
from .schema import Cell, CodeCell, CellMetadata, Output, ExecuteResult, DisplayData, Stream, Error, Notebook, ContentResponseModel

def locate_idx_for_cell_with_given_id(notebook_model: Notebook, cell_id: str) -> Optional[int]:
    cell_idx_to_replace = next(
        (idx for idx, cell in enumerate(notebook_model.cells) if cell.id == cell_id),
        None
    )

    return cell_idx_to_replace