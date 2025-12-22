class ProbeResult:
    
    def __init__(self) -> None:
        self.result = None
        self.success = False
        self.error_message = None

    def set_result(self, result):
        self.result = result

    def set_success(self, success):
        self.success = success

    def set_error_message(self, error_message):
        self.error_message = error_message

    def get_result(self):
        return self.result

    def is_success(self):
        return self.success

    def get_error_message(self):
        return self.error_message