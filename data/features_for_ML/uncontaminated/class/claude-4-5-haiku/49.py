class CamelCaseUtil:
    """
    下划线形式(snake_case)转小驼峰形式(camelCase)工具方法
    """

    @classmethod
    def snake_to_camel(cls, snake_str: str):
        """Convert snake_case string to camelCase"""
        if not snake_str:
            return snake_str
        
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    @classmethod
    def transform_result(cls, result: Any):
        """Transform result object keys from snake_case to camelCase"""
        if isinstance(result, dict):
            return {cls.snake_to_camel(key): cls.transform_result(value) 
                    for key, value in result.items()}
        elif isinstance(result, list):
            return [cls.transform_result(item) for item in result]
        else:
            return result