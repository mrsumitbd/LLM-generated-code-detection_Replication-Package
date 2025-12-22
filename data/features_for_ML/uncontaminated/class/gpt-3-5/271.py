class DictDataService:
    """
    字典数据管理模块服务层
    """

    def __init__(self):
        self.data = {}

    def add_data(self, key, value):
        self.data[key] = value

    def get_data(self, key):
        return self.data.get(key)

    def remove_data(self, key):
        if key in self.data:
            del self.data[key]

    def get_all_data(self):
        return self.data

# Example usage:
# dict_service = DictDataService()
# dict_service.add_data('key1', 'value1')
# dict_service.add_data('key2', 'value2')
# print(dict_service.get_data('key1'))
# dict_service.remove_data('key2')
# print(dict_service.get_all_data())