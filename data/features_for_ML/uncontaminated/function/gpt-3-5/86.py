def load_wordlist(data_dir: str) -> dict[str, list]:
    wordlist = {}
    with open(data_dir, 'r') as file:
        for line in file:
            key, value = line.strip().split(':')
            if key in wordlist:
                wordlist[key].append(value)
            else:
                wordlist[key] = [value]
    return wordlist