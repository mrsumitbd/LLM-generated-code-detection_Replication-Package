import json
import os
import tempfile

def create_tmp_json(data_dict, json_path):
        # 创建一个临时文件用于存储修改后的 JSON 数据
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json',
                                         dir=tempfile.mkdtemp()) as tmp_file:
            # 将修改后的数据写入临时文件
            json.dump(data_dict, tmp_file, indent=4)
            temp_json_path = tmp_file.name
        # 提取出临时文件所在的目录
        temp_dir = os.path.dirname(temp_json_path)
        # 获取文件名
        filename = os.path.basename(json_path)
        new_file_path = os.path.join(temp_dir, filename)
        # 重命名临时文件
        os.rename(temp_json_path, new_file_path)
        return temp_dir, new_file_path