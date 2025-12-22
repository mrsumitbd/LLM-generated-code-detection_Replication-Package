def load_csv_dir(
    dir_path: str,
    encoding: str = defs.FILE_ENCODING,
    text_tag: str = defs.TEXT_COLUMN,
    metadata_tags: list[str] | None = None,
    max_text_length: int | None = None,
) -> list[Document]:
    """Load a directory of CSV files and return a list of Document objects."""
    documents = []
    for file_path in os.listdir(dir_path):
        if file_path.endswith('.csv'):
            file_path = os.path.join(dir_path, file_path)
            with open(file_path, 'r', encoding=encoding) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    text = row[text_tag]
                    if max_text_length is not None:
                        text = text[:max_text_length]
                    metadata = {tag: row[tag] for tag in metadata_tags or []}
                    document = Document(text=text, metadata=metadata)
                    documents.append(document)
    return documents