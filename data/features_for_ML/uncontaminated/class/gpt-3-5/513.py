class ShadeMergeResponse:

    def __init__(self, result: Any, success: bool):
        self.result = result
        self.success = success

    def to_json(self) -> dict:
        return {
            "result": self.result,
            "success": self.success
        }