def filter_solutions(dataset):
    # First filter out incorrect responses.
    filtered_dataset = [solution for solution in dataset if solution['is_correct']]
    return filtered_dataset