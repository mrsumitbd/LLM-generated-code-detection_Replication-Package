import json

class JsonUtil:

    @staticmethod
    def write_data(data, data_path):
        with open(data_path, 'w') as file:
            json.dump(data, file)

    @staticmethod
    def read_data(data_path):
        with open(data_path, 'r') as file:
            return json.load(file)

    @staticmethod
    def read_all_data(data_path_dir) -> list[dict]:
        all_data = []
        for file_name in os.listdir(data_path_dir):
            if file_name.endswith('.json'):
                with open(os.path.join(data_path_dir, file_name), 'r') as file:
                    data = json.load(file)
                    all_data.append(data)
        return all_data

    @staticmethod
    def create_tmp_json(data_dict, json_path):
        with open(json_path, 'w') as file:
            json.dump(data_dict, file)

    @staticmethod
    def rewrite_template_json(jsonpath, extend_args: dict[str, list] = None, **kwargs):
        with open(jsonpath, 'r') as file:
            template_data = json.load(file)
        
        if extend_args:
            for key, value in extend_args.items():
                template_data[key] = value
        
        for key, value in kwargs.items():
            template_data[key] = value
        
        with open(jsonpath, 'w') as file:
            json.dump(template_data, file)