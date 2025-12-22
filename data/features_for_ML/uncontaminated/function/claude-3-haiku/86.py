import os

def load_wordlist(data_dir: str) -> dict[str, list]:
    """
    Return a dictionary of wordlist with the following format:
        ke:
        ek:
    """
    wordlist = {}
    for filename in os.listdir(data_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(data_dir, filename), 'r') as file:
                words = [word.strip() for word in file.readlines()]
                wordlist[filename[:-4]] = words
    return wordlist