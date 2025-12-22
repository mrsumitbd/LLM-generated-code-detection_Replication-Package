def load_csv_dir(
    dir_path: str,
    encoding: str = defs.FILE_ENCODING,
    text_tag: str = defs.TEXT_COLUMN,
    metadata_tags: list[str] | None = None,
    max_text_length: int | None = None,
) -> list[Document]:
    import os
    import pandas as pd
    from Document import Document
    
    documents = []
    
    for file_name in os.listdir(dir_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(dir_path, file_name)
            df = pd.read_csv(file_path, encoding=encoding)
            
            for index, row in df.iterrows():
                text = row[text_tag]
                metadata = {tag: row[tag] for tag in metadata_tags} if metadata_tags else None
                if max_text_length and len(text) > max_text_length:
                    text = text[:max_text_length]
                
                document = Document(text, metadata)
                documents.append(document)
    
    return documents