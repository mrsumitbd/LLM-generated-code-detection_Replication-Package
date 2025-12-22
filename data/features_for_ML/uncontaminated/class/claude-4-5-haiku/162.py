import json
import os
from pathlib import Path


class JsonUtil:

    @staticmethod
    def write_data(data, data_path):
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def read_data(data_path):
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def read_all_data(data_path_dir) -> list[dict]:
        data_list = []
        if not os.path.isdir(data_path_dir):
            return data_list
        
        for filename in os.listdir(data_path_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(data_path_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        data_list.append(data)
                except (json.JSONDecodeError, IOError):
                    continue
        
        return data_list

    @staticmethod
    def create_tmp_json(data_dict, json_path):
        os.makedirs(os.path.dirname(json_path) or '.', exist_ok=True)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, indent=4)

    @staticmethod
    def rewrite_template_json(jsonpath, extend_arges: dict[str, list] = None, **kwargs):
        with open(jsonpath, 'r', encoding='utf-8') as f:
            template_data = json.load(f)
        
        if extend_arges:
            for key, value in extend_arges.items():
                if key in template_data and isinstance(template_data[key], list):
                    template_data[key].extend(value)
                else:
                    template_data[key] = value
        
        for key, value in kwargs.items():
            template_data[key] = value
        
        with open(jsonpath, 'w', encoding='utf-8') as f:
            json.dump(template_data, f, ensure_ascii=False, indent=4)