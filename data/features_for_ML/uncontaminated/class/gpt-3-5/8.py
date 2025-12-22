class TableCell:
    def __init__(self, value):
        self.value = value

class Table:
    def __init__(self):
        self.cells = {}

    def get_cell(self, column: int, row: int) -> TableCell:
        return self.cells.get((column, row))

    def set_cell(self, column: int, row: int, cell: TableCell) -> None:
        self.cells[(column, row)] = cell

    def clear_cell(self, column: int, row: int) -> None:
        if (column, row) in self.cells:
            del self.cells[(column, row)]

    def clear_cells(self, start_column: int, start_row: int, end_column: int, end_row: int) -> None:
        for column in range(start_column, end_column + 1):
            for row in range(start_row, end_row + 1):
                self.clear_cell(column, row)

    def merge_cells(self, start_column: int, start_row: int, end_column: int, end_row: int) -> None:
        for column in range(start_column, end_column + 1):
            for row in range(start_row, end_row + 1):
                if (column, row) != (start_column, start_row):
                    self.clear_cell(column, row)