import os

def load_book_content(setup: str, data_dir: str) -> str:
    """
    Loads the content of a book from a file in the specified data directory.

    Args:
        setup (str): The setup configuration for the book.
        data_dir (str): The directory where the book data is stored.

    Returns:
        str: The content of the book.
    """
    book_file = os.path.join(data_dir, f"{setup}.txt")
    with open(book_file, "r") as file:
        book_content = file.read()
    return book_content