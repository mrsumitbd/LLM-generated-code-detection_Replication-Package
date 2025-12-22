class UserService:
    """
    用户服务类。
    管理用户信息和授权信息。
    """

    def __init__(self, dbkey: str):
        self.dbkey = dbkey
        self._user_info = None
        self._raw_data = {}

    def get_user_info(self):
        return self._user_info

    def set_user_info(self, user_info: UserInfo):
        self._user_info = user_info

    def update_raw_key(self, key: str, value: str):
        self._raw_data[key] = value

    def get_raw_key(self, key: str) -> Optional[str]:
        return self._raw_data.get(key)

    def dump_to_file(self):
        import json
        import os
        
        data = {
            'dbkey': self.dbkey,
            'user_info': self._user_info.__dict__ if self._user_info else None,
            'raw_data': self._raw_data
        }
        
        filename = f"{self.dbkey}_user_service.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)