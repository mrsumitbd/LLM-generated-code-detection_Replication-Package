def convert_txt_to_json(txt_filepath: str, json_filepath: str, method: str, model: str, directory_path: str) -> None:
    import json

    data = {}
    with open(txt_filepath, 'r') as txt_file:
        lines = txt_file.readlines()
        data['method'] = method
        data['model'] = model
        data['directory_path'] = directory_path
        data['results'] = []

        for line in lines:
            parts = line.strip().split(',')
            result = {
                'attribute1': parts[0],
                'attribute2': parts[1],
                'attribute3': parts[2]
            }
            data['results'].append(result)

    with open(json_filepath, 'w') as json_file:
        json.dump(data, json_file)