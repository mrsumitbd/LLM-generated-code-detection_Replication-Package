class CamelCaseUtil:
    """
    下划线形式(snake_case)转小驼峰形式(camelCase)工具方法
    """

    @classmethod
    def snake_to_camel(cls, snake_str: str):
        words = snake_str.split('_')
        camel_case = words[0] + ''.join(word.capitalize() for word in words[1:])
        return camel_case

    @classmethod
    def transform_result(cls, result: Any):
        if isinstance(result, dict):
            return {cls.snake_to_camel(key): value for key, value in result.items()}
        elif isinstance(result, list):
            return [cls.transform_result(item) for item in result]
        else:
            return result