def get_predictions_from_file(predictions_path: str, dataset_name: str, split: str):
    predictions = {}
    with open(predictions_path, 'r') as file:
        for line in file:
            data = line.strip().split(',')
            if data[0] == dataset_name and data[1] == split:
                predictions[data[2]] = float(data[3])
    return predictions