class SpreadsheetContext:
    """Context for Google Spreadsheet service"""

    def __init__(self, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id

    def get_spreadsheet_id(self):
        return self.spreadsheet_id

    def set_spreadsheet_id(self, new_id):
        self.spreadsheet_id = new_id

    def read_data(self, range):
        # Code to read data from the specified range in the spreadsheet
        pass

    def write_data(self, range, data):
        # Code to write data to the specified range in the spreadsheet
        pass