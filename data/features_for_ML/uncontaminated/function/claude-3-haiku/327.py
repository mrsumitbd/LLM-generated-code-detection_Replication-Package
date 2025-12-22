def _select_choice(choices, rls_data):
    if not choices:
        return None

    if not rls_data:
        return choices[0]

    max_score = 0
    selected_choice = None

    for choice in choices:
        score = 0
        for rule in rls_data:
            if rule['condition'](choice):
                score += rule['score']
        if score > max_score:
            max_score = score
            selected_choice = choice

    return selected_choice