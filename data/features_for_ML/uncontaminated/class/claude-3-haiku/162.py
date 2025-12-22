import json
import os
import tempfile

class JsonUtil:

    @staticmethod
    def write_data(data, data_path):
        with open(data_path, 'w') as f:
            json.dump(data, f)

    @staticmethod
    def read_data(data_path):
        with open(data_path, 'r') as f:
            return json.load(f)

    @staticmethod
    def read_all_data(data_path_dir) -> list[dict]:
        data = []
        for filename in os.listdir(data_path_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(data_path_dir, filename)
                data.append(JsonUtil.read_data(file_path))
        return data

    @staticmethod
    def create_tmp_json(data_dict, json_path):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp_file:
            json.dump(data_dict, tmp_file)
            tmp_file_path = tmp_file.name
        os.rename(tmp_file_path, json_path)

    @staticmethod
    def rewrite_template_json(jsonpath, extend_arges: dict[str, list] = None, **kwargs):
        with open(jsonpath, 'r') as f:
            template = json.load(f)

        if extend_arges:
            for key, values in extend_arges.items():
                template[key].extend(values)

        for key, value in kwargs.items():
            template[key] = value

        with open(jsonpath, 'w') as f:
            json.dump(template, f, indent=4)