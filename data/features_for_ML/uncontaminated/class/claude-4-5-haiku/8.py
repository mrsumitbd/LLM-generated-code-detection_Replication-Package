class Table:
    def __init__(self):
        self._cells = {}
        self._merged_regions = []

    def get_cell(self, column: int, row: int) -> TableCell:
        if (column, row) in self._cells:
            return self._cells[(column, row)]
        return TableCell()

    def set_cell(self, column: int, row: int, cell: TableCell) -> None:
        self._cells[(column, row)] = cell

    def clear_cell(self, column: int, row: int) -> None:
        if (column, row) in self._cells:
            del self._cells[(column, row)]

    def clear_cells(self, start_column: int, start_row: int, end_column: int, end_row: int) -> None:
        keys_to_delete = []
        for col in range(start_column, end_column + 1):
            for row in range(start_row, end_row + 1):
                if (col, row) in self._cells:
                    keys_to_delete.append((col, row))
        for key in keys_to_delete:
            del self._cells[key]

    def merge_cells(self, start_column: int, start_row: int, end_column: int, end_row: int) -> None:
        self._merged_regions.append({
            'start_column': start_column,
            'start_row': start_row,
            'end_column': end_column,
            'end_row': end_row
        })


class TableCell:
    def __init__(self):
        self.value = None