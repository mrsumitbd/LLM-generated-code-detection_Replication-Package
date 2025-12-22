class TableCell:
    """
    Simple cell representation.  A cell can hold arbitrary content and may be part of a merged region.
    """
    def __init__(self, content=None, merged=False, region=None):
        self.content = content
        self.merged = merged          # True if this cell is the top-left of a merged region
        self.region = region          # (start_col, start_row, end_col, end_row) if merged

    def __repr__(self):
        if self.merged:
            return f"<MergedCell {self.region}>"
        return f"<Cell {self.content!r}>"


class Table:
    """
    2‑D table that supports cell access, clearing, and merging.
    Cells are stored in a dictionary keyed by (column, row).
    """
    def __init__(self):
        self._cells = {}  # key: (col, row) -> TableCell

    def _normalize_region(self, start_column, start_row, end_column, end_row):
        """Return region with start <= end for both axes."""
        sc, sr, ec, er = start_column, start_row, end_column, end_row
        if sc > ec:
            sc, ec = ec, sc
        if sr > er:
            sr, er = er, sr
        return sc, sr, ec, er

    def get_cell(self, column: int, row: int) -> TableCell:
        return self._cells.get((column, row))

    def set_cell(self, column: int, row: int, cell: TableCell) -> None:
        self._cells[(column, row)] = cell

    def clear_cell(self, column: int, row: int) -> None:
        self._cells.pop((column, row), None)

    def clear_cells(self, start_column: int, start_row: int, end_column: int, end_row: int) -> None:
        sc, sr, ec, er = self._normalize_region(start_column, start_row, end_column, end_row)
        for c in range(sc, ec + 1):
            for r in range(sr, er + 1):
                self._cells.pop((c, r), None)

    def merge_cells(self, start_column: int, start_row: int, end_column: int, end_row: int) -> None:
        sc, sr, ec, er = self._normalize_region(start_column, start_row, end_column, end_row)
        merged_cell = TableCell(merged=True, region=(sc, sr, ec, er))
        for c in range(sc, ec + 1):
            for r in range(sr, er + 1):
                self._cells[(c, r)] = merged_cell