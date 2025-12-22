class DoAccountAuthResponse:

    def __init__(self, data: dict) -> None:
        self.data = data
        self.success = data.get("success", False)
        self.message = data.get("message", "")
        self.auth_token = data.get("auth_token")
        self.user_id = data.get("user_id")
        self.username = data.get("username")
        self.email = data.get("email")
        self.error_code = data.get("error_code")
        self.error_details = data.get("error_details")

    def __str__(self) -> str:
        return f"DoAccountAuthResponse(success={self.success}, message={self.message})"

    def __repr__(self) -> str:
        return self.__str__()

    def is_successful(self) -> bool:
        return self.success

    def get_auth_token(self) -> str:
        return self.auth_token

    def get_user_id(self) -> str:
        return self.user_id

    def get_username(self) -> str:
        return self.username

    def get_email(self) -> str:
        return self.email

    def get_error_code(self) -> str:
        return self.error_code

    def get_error_details(self) -> str:
        return self.error_details

    def get_message(self) -> str:
        return self.message