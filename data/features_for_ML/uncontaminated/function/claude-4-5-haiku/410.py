def load_csv_dir(
    dir_path: str,
    encoding: str = defs.FILE_ENCODING,
    text_tag: str = defs.TEXT_COLUMN,
    metadata_tags: list[str] | None = None,
    max_text_length: int | None = None,
) -> list[Document]:
    """Load a directory of CSV files and return a list of Document objects."""
    import os
    import csv
    from pathlib import Path
    
    documents = []
    dir_path = Path(dir_path)
    
    if not dir_path.is_dir():
        raise ValueError(f"Directory not found: {dir_path}")
    
    csv_files = sorted(dir_path.glob("*.csv"))
    
    for csv_file in csv_files:
        try:
            with open(csv_file, "r", encoding=encoding) as f:
                reader = csv.DictReader(f)
                
                if reader.fieldnames is None:
                    continue
                
                if text_tag not in reader.fieldnames:
                    continue
                
                for row in reader:
                    text = row.get(text_tag, "").strip()
                    
                    if not text:
                        continue
                    
                    if max_text_length and len(text) > max_text_length:
                        text = text[:max_text_length]
                    
                    metadata = {}
                    if metadata_tags:
                        for tag in metadata_tags:
                            if tag in row:
                                metadata[tag] = row[tag]
                    else:
                        for key, value in row.items():
                            if key != text_tag:
                                metadata[key] = value
                    
                    doc = Document(
                        text=text,
                        metadata=metadata,
                        source=str(csv_file)
                    )
                    documents.append(doc)
        
        except Exception as e:
            continue
    
    return documents