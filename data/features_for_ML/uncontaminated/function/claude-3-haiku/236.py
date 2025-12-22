def get_modal_prefix():
    import re

    modal_prefixes = {
        "can": "can",
        "could": "could",
        "may": "may",
        "might": "might",
        "must": "must",
        "shall": "shall",
        "should": "should",
        "will": "will",
        "would": "would"
    }

    user_input = input("Enter a sentence: ")
    for prefix in modal_prefixes:
        if re.search(r'\b' + prefix + r'\b', user_input, re.IGNORECASE):
            return modal_prefixes[prefix]
    return None