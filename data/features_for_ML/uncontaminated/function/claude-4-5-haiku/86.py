def load_wordlist(data_dir: str) -> dict[str, list]:
    """
    Return a dictionary of wordlist with the following format:
        ke:
        ek:
    """
    import os
    import json
    
    wordlist = {}
    
    # Look for wordlist files in the data directory
    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(data_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                wordlist.update(data)
    
    # If no JSON files found, try to load from text files
    if not wordlist:
        for filename in os.listdir(data_dir):
            if filename.startswith('ke') or filename.startswith('ek'):
                filepath = os.path.join(data_dir, filename)
                key = filename.split('.')[0]
                with open(filepath, 'r', encoding='utf-8') as f:
                    wordlist[key] = [line.strip() for line in f.readlines() if line.strip()]
    
    return wordlist