def load_book_content(setup: str, data_dir: str) -> str:
    file_path = os.path.join(data_dir, setup)
    with open(file_path, 'r') as file:
        content = file.read()
    return content