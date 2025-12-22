from typing import Optional

class UserInfo:
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

class UserService:
    """
    用户服务类。
    管理用户信息和授权信息。
    """

    def __init__(self, dbkey: str):
        self.dbkey = dbkey
        self.user_info = None
        self.raw_data = {}

    def get_user_info(self):
        return self.user_info

    def set_user_info(self, user_info: UserInfo):
        self.user_info = user_info

    def update_raw_key(self, key: str, value: str):
        self.raw_data[key] = value

    def get_raw_key(self, key: str) -> Optional[str]:
        return self.raw_data.get(key)

    def dump_to_file(self):
        with open('user_data.txt', 'w') as file:
            file.write(f"DB Key: {self.dbkey}\n")
            file.write(f"User Info: {self.user_info.username}, {self.user_info.email}\n")
            file.write("Raw Data:\n")
            for key, value in self.raw_data.items():
                file.write(f"{key}: {value}\n")