class TableCell:
    def __init__(self, value: str = ""):
        self.value = value

class Table:
    def __init__(self):
        self.cells = {}

    def get_cell(self, column: int, row: int) -> TableCell:
        key = (column, row)
        if key in self.cells:
            return self.cells[key]
        else:
            cell = TableCell()
            self.cells[key] = cell
            return cell

    def set_cell(self, column: int, row: int, cell: TableCell) -> None:
        self.cells[(column, row)] = cell

    def clear_cell(self, column: int, row: int) -> None:
        key = (column, row)
        if key in self.cells:
            del self.cells[key]

    def clear_cells(self, start_column: int, start_row: int, end_column: int, end_row: int) -> None:
        for column in range(start_column, end_column + 1):
            for row in range(start_row, end_row + 1):
                self.clear_cell(column, row)

    def merge_cells(self, start_column: int, start_row: int, end_column: int, end_row: int) -> None:
        merged_cell = TableCell()
        for column in range(start_column, end_column + 1):
            for row in range(start_row, end_row + 1):
                self.set_cell(column, row, merged_cell)