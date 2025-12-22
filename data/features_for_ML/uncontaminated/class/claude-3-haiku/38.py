import json
from typing import Optional

class UserInfo:
    def __init__(self, name: str, email: str, phone: str):
        self.name = name
        self.email = email
        self.phone = phone

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
        return self.raw_data.get(key, None)

    def dump_to_file(self):
        data = {
            "dbkey": self.dbkey,
            "user_info": {
                "name": self.user_info.name,
                "email": self.user_info.email,
                "phone": self.user_info.phone
            },
            "raw_data": self.raw_data
        }
        with open(f"{self.dbkey}.json", "w") as f:
            json.dump(data, f)