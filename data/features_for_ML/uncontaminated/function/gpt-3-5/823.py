def build_search_index(messages: List[Dict], patterns: List[Dict], errors: List[Dict]) -> str:
    index = {}
    for message in messages:
        tokens = message['text'].split()
        for token in tokens:
            if token not in index:
                index[token] = []
            index[token].append(message['id'])
    
    for pattern in patterns:
        tokens = pattern['text'].split()
        for token in tokens:
            if token not in index:
                index[token] = []
            index[token].append(pattern['id'])
    
    for error in errors:
        tokens = error['text'].split()
        for token in tokens:
            if token not in index:
                index[token] = []
            index[token].append(error['id'])
    
    search_index = []
    for token, ids in index.items():
        search_index.append(f"{token}: {', '.join(map(str, ids))}")
    
    return '\n'.join(search_index)