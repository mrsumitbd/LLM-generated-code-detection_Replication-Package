from pathlib import Path
import benchmark_qed.config.defaults as defs
from benchmark_qed.autod.data_model.document import Document

def load_csv_dir(
    dir_path: str,
    encoding: str = defs.FILE_ENCODING,
    text_tag: str = defs.TEXT_COLUMN,
    metadata_tags: list[str] | None = None,
    max_text_length: int | None = None,
) -> list[Document]:
    """Load a directory of CSV files and return a list of Document objects."""
    documents: list[Document] = []
    for file_path in Path(dir_path).rglob("*.csv"):
        documents.extend(
            load_csv_doc(
                file_path=str(file_path),
                encoding=encoding,
                text_tag=text_tag,
                metadata_tags=metadata_tags,
                max_text_length=max_text_length,
            )
        )

    for index, document in enumerate(documents):
        document.short_id = str(index)

    return documents