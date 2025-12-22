class DictDataService:
    """
    字典数据管理模块服务层
    """

    def __init__(self, dict_data_repo):
        self.dict_data_repo = dict_data_repo

    def get_dict_data(self, dict_type):
        return self.dict_data_repo.get_dict_data(dict_type)

    def create_dict_data(self, dict_type, data):
        return self.dict_data_repo.create_dict_data(dict_type, data)

    def update_dict_data(self, dict_type, data):
        return self.dict_data_repo.update_dict_data(dict_type, data)

    def delete_dict_data(self, dict_type, data_id):
        return self.dict_data_repo.delete_dict_data(dict_type, data_id)