from __future__ import annotations

import threading
from typing import Any, Dict, Iterable, List, Optional, Tuple


class DictDataError(Exception):
    """Base exception for DictDataService."""


class DictDataNotFoundError(DictDataError):
    """Raised when a requested key does not exist."""


class DictDataAlreadyExistsError(DictDataError):
    """Raised when attempting to add a key that already exists."""


class DictDataService:
    """
    字典数据管理模块服务层

    该服务层提供对字典数据的增删改查操作，支持线程安全访问。
    数据以键值对形式存储，每个键对应一个包含 ``value`` 与可选 ``description`` 的字典。
    """

    def __init__(self, initial_data: Optional[Dict[str, Dict[str, Any]]] = None) -> None:
        """
        初始化服务层。

        :param initial_data: 可选的初始数据映射，键为字符串，值为包含 ``value`` 与 ``description`` 的字典。
        """
        self._lock = threading.RLock()
        self._data: Dict[str, Dict[str, Any]] = {}
        if initial_data:
            for k, v in initial_data.items():
                self._data[k] = {"value": v.get("value"), "description": v.get("description")}

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------
    def add(self, key: str, value: Any, description: Optional[str] = None) -> None:
        """
        添加一条字典数据。

        :param key: 字典键，必须唯一。
        :param value: 对应的值。
        :param description: 可选描述信息。
        :raises DictDataAlreadyExistsError: 如果键已存在。
        """
        with self._lock:
            if key in self._data:
                raise DictDataAlreadyExistsError(f"Key '{key}' already exists.")
            self._data[key] = {"value": value, "description": description}

    def get(self, key: str) -> Dict[str, Any]:
        """
        根据键获取字典数据。

        :param key: 要查询的键。
        :return: 包含 ``value`` 与 ``description`` 的字典。
        :raises DictDataNotFoundError: 如果键不存在。
        """
        with self._lock:
            if key not in self._data:
                raise DictDataNotFoundError(f"Key '{key}' not found.")
            return self._data[key].copy()

    def update(
        self,
        key: str,
        value: Optional[Any] = None,
        description: Optional[str] = None,
    ) -> None:
        """
        更新已有字典数据。

        :param key: 要更新的键。
        :param value: 新的值，若为 ``None`` 则不更新。
        :param description: 新的描述，若为 ``None`` 则不更新。
        :raises DictDataNotFoundError: 如果键不存在。
        """
        with self._lock:
            if key not in self._data:
                raise DictDataNotFoundError(f"Key '{key}' not found.")
            if value is not None:
                self._data[key]["value"] = value
            if description is not None:
                self._data[key]["description"] = description

    def delete(self, key: str) -> None:
        """
        删除指定键的数据。

        :param key: 要删除的键。
        :raises DictDataNotFoundError: 如果键不存在。
        """
        with self._lock:
            if key not in self._data:
                raise DictDataNotFoundError(f"Key '{key}' not found.")
            del self._data[key]

    # ------------------------------------------------------------------
    # 查询
    # ------------------------------------------------------------------
    def list_all(self) -> List[Tuple[str, Dict[str, Any]]]:
        """
        返回所有键值对的列表。

        :return: 形如 ``[(key, {'value': ..., 'description': ...}), ...]`` 的列表。
        """
        with self._lock:
            return [(k, v.copy()) for k, v in self._data.items()]

    def find_by_value(self, value: Any) -> List[str]:
        """
        根据值查找所有匹配的键。

        :param value: 要匹配的值。
        :return: 所有匹配键的列表。
        """
        with self._lock:
            return [k for k, v in self._data.items() if v["value"] == value]

    def get_by_type(self, type_prefix: str) -> List[Tuple[str, Dict[str, Any]]]:
        """
        根据键前缀（类型）获取所有匹配的数据。

        键的格式可为 ``<type>:<key>``，此方法会返回所有以 ``type_prefix`` 开头的键。

        :param type_prefix: 键前缀，例如 ``'config'``。
        :return: 匹配键值对的列表。
        """
        with self._lock:
            return [
                (k, v.copy())
                for k, v in self._data.items()
                if k.startswith(f"{type_prefix}:")
            ]

    # ------------------------------------------------------------------
    # 便利方法
    # ------------------------------------------------------------------
    def __contains__(self, key: str) -> bool:
        with self._lock:
            return key in self._data

    def __len__(self) -> int:
        with self._lock:
            return len(self._data)

    def __iter__(self):
        with self._lock:
            return iter(self._data.copy())

    def __repr__(self) -> str:
        with self._lock:
            return f"<DictDataService {len(self._data)} items>"

    # ------------------------------------------------------------------
    # 备份与恢复
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Dict[str, Any]]:
        """
        将内部数据导出为普通字典。

        :return: 深拷贝后的数据字典。
        """
        with self._lock:
            return {k: v.copy() for k, v in self._data.items()}

    def load_from_dict(self, data: Dict[str, Dict[str, Any]]) -> None:
        """
        用给定的数据替换当前数据。

        :param data: 形如 ``{key: {'value': ..., 'description': ...}, ...}`` 的字典。
        """
        with self._lock:
            self._data = {k: {"value": v.get("value"), "description": v.get("description")} for k, v in data.items()}