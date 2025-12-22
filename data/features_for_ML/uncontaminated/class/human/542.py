
class DoAccountAuthResponse:
    def __init__(self, data: dict) -> None:
        self.status = getValue(data, ["status"])
        if self.status == 1:
            self.token = getValue(data, ["token"])
            self.refresh_token = getValue(data, ["refresh_token", "refreshtoken"])
            self.user = DoAccountAuthResponseUser(data["user"])

    token: str
    status: int
    refresh_token: str
    user: DoAccountAuthResponseUser