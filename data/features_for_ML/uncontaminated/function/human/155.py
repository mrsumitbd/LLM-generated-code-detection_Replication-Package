def filter_solutions(dataset):
    # First filter out incorrect responses.
    for key in dataset:
        problem = dataset[key]
        keys_to_filter = []
        for response_key in problem["responses"]:
            if not problem["responses"][response_key]["correctness"]:
                keys_to_filter.append(response_key)
        for k in keys_to_filter:
            del problem["responses"][k]
            del problem["token_usages"][k]

    # Next, filter out examples with <2 correct responses.
    keys_to_filter = []
    for key in dataset:
        problem = dataset[key]
        if len(problem["responses"]) < 2:
            keys_to_filter.append(key)
    for k in keys_to_filter:
        del dataset[k]

    # Finally, filter for the shortest and longest solutions for each sample.
    for key in dataset:
        problem = dataset[key]
        token_usages = problem["token_usages"]
        shortest_key, shortest_entry = min(
            token_usages.items(), key=lambda x: x[1]["completion_tokens"]
        )
        longest_key, longest_entry = max(
            token_usages.items(), key=lambda x: x[1]["completion_tokens"]
        )
        problem["token_usages"] = {
            "shortest": shortest_entry,
            "longest": longest_entry,
        }
        new_responses = {
            "shortest": problem["responses"][shortest_key],
            "longest": problem["responses"][longest_key],
        }
        problem["responses"] = new_responses

    return dataset