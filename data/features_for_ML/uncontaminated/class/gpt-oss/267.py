from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

class PropertyList:
    """
    属性列表.
    """

    def __init__(self, properties: Optional[List["Property"]] = None):
        """
        初始化属性列表。

        :param properties: 可选的 Property 对象列表。
        """
        self._props: Dict[str, "Property"] = {}
        if properties:
            for prop in properties:
                self.add_property(prop)

    def add_property(self, prop: "Property"):
        """
        添加一个 Property 到列表。

        :param prop: 要添加的 Property 对象。
        """
        if not hasattr(prop, "name"):
            raise TypeError("Property 必须具有 'name' 属性")
        self._props[prop.name] = prop

    def __getitem__(self, name: str) -> "Property":
        """
        根据属性名获取 Property。

        :param name: 属性名。
        :return: 对应的 Property 对象。
        """
        return self._props[name]

    def get_required(self) -> List[str]:
        """
        获取所有必需属性的名称列表。

        :return: 必需属性名列表。
        """
        return [name for name, prop in self._props.items() if getattr(prop, "required", False)]

    def to_json(self) -> Dict[str, Any]:
        """
        将属性列表序列化为 JSON 兼容的字典。

        :return: 字典形式的属性描述。
        """
        result: Dict[str, Any] = {}
        for name, prop in self._props.items():
            if hasattr(prop, "to_json") and callable(prop.to_json):
                result[name] = prop.to_json()
            else:
                # 直接使用属性的 __dict__，但排除不可序列化字段
                d = {}
                for k, v in prop.__dict__.items():
                    try:
                        import json
                        json.dumps(v)
                        d[k] = v
                    except Exception:
                        pass
                result[name] = d
        return result

    def parse_arguments(self, arguments: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        解析并验证传入的参数字典。

        :param arguments: 传入的参数字典，键为属性名，值为对应值。
        :return: 解析后的参数字典。
        :raises ValueError: 当必需属性缺失或类型转换失败时。
        """
        if arguments is None:
            arguments = {}

        parsed: Dict[str, Any] = {}
        for name, prop in self._props.items():
            if name in arguments:
                raw_value = arguments[name]
                # 如果 Property 定义了 parse 方法，使用它
                if hasattr(prop, "parse") and callable(prop.parse):
                    try:
                        parsed_value = prop.parse(raw_value)
                    except Exception as exc:
                        raise ValueError(f"属性 '{name}' 解析失败: {exc}") from exc
                else:
                    # 尝试使用 type 转换
                    prop_type = getattr(prop, "type", None)
                    if prop_type and callable(prop_type):
                        try:
                            parsed_value = prop_type(raw_value)
                        except Exception as exc:
                            raise ValueError(f"属性 '{name}' 转换为 {prop_type} 失败: {exc}") from exc
                    else:
                        parsed_value = raw_value
                parsed[name] = parsed_value
            else:
                # 属性不存在于传入参数
                if getattr(prop, "required", False):
                    raise ValueError(f"缺少必需属性: '{name}'")
                # 使用默认值（如果存在）
                if hasattr(prop, "default"):
                    parsed[name] = prop.default
        return parsed