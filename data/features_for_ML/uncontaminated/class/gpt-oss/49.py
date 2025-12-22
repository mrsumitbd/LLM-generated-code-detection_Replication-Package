from typing import Any, Dict, List, Tuple, Union

class CamelCaseUtil:
    """
    下划线形式(snake_case)转小驼峰形式(camelCase)工具方法
    """

    @classmethod
    def snake_to_camel(cls, snake_str: str) -> str:
        """
        Convert a snake_case string to camelCase.
        """
        if not isinstance(snake_str, str):
            return snake_str
        parts = snake_str.split('_')
        if not parts:
            return snake_str
        # first part stays lowercase, subsequent parts capitalize first letter
        return parts[0] + ''.join(word.capitalize() for word in parts[1:])

    @classmethod
    def transform_result(cls, result: Any) -> Any:
        """
        Recursively transform dictionary keys from snake_case to camelCase.
        Lists, tuples, sets, and other iterables are processed element-wise.
        Non-iterable values are returned unchanged.
        """
        if isinstance(result, dict):
            new_dict: Dict[str, Any] = {}
            for key, value in result.items():
                new_key = cls.snake_to_camel(key)
                new_dict[new_key] = cls.transform_result(value)
            return new_dict
        elif isinstance(result, list):
            return [cls.transform_result(item) for item in result]
        elif isinstance(result, tuple):
            return tuple(cls.transform_result(item) for item in result)
        elif isinstance(result, set):
            return {cls.transform_result(item) for item in result}
        else:
            return result