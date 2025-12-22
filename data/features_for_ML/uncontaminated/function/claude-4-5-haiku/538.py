def write(filename: str, content: str):
    with open(filename, 'w') as f:
        f.write(content)