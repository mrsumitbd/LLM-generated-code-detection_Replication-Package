def _select_choice(choices, rls_data):
    selected_choice = None
    for choice in choices:
        if choice['id'] == rls_data['choice_id']:
            selected_choice = choice
            break
    return selected_choice