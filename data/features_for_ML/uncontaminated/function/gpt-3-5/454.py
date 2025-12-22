def convert(path: str) -> None:
    with open(path, 'r') as file:
        data = file.read()
    
    with open(path, 'w') as file:
        file.write(data.upper())