import json
import os
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Optional, Dict, Any


@dataclass
class UserInfo:
    """
    Simple user information container.
    Additional fields can be added as needed.
    """
    name: str = ""
    email: str = ""
    # Store any extra attributes in a dict
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        # Merge extra into top level
        data.update(data.pop("extra", {}))
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserInfo":
        # Separate known fields from extras
        known = {k: data.pop(k) for k in ("name", "email") if k in data}
        return cls(**known, extra=data)


class UserService:
    """
    用户服务类。
    管理用户信息和授权信息。
    """

    def __init__(self, dbkey: str):
        """
        初始化用户服务，加载或创建数据库文件。

        :param dbkey: 数据库文件路径
        """
        self._db_path = Path(dbkey)
        self._data: Dict[str, Any] = {"user_info": None, "raw": {}}
        if self._db_path.exists():
            try:
                with self._db_path.open("r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except Exception:
                # 如果文件损坏，重新初始化
                self._data = {"user_info": None, "raw": {}}

    def get_user_info(self) -> Optional[UserInfo]:
        """
        获取当前用户信息。

        :return: UserInfo 实例或 None
        """
        ui = self._data.get("user_info")
        if ui is None:
            return None
        return UserInfo.from_dict(ui)

    def set_user_info(self, user_info: UserInfo):
        """
        设置用户信息。

        :param user_info: UserInfo 实例
        """
        self._data["user_info"] = user_info.to_dict()

    def update_raw_key(self, key: str, value: str):
        """
        更新原始键值对。

        :param key: 键
        :param value: 值
        """
        self._data["raw"][key] = value

    def get_raw_key(self, key: str) -> Optional[str]:
        """
        获取原始键对应的值。

        :param key: 键
        :return: 值或 None
        """
        return self._data["raw"].get(key)

    def dump_to_file(self):
        """
        将当前数据持久化到文件。
        """
        # 确保父目录存在
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._db_path.open("w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)