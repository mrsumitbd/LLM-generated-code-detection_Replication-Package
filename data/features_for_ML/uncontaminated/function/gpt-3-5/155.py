def filter_solutions(dataset):
    filtered_dataset = []
    for data in dataset:
        if data['response'] == data['expected']:
            filtered_dataset.append(data)
    return filtered_dataset