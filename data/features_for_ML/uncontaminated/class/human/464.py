from typing import Annotated
from pydantic import Field

class SaveDocumentOutput:
    """Output of the save_docling_document tool."""

    md_file: Annotated[
        str,
        Field(
            description="The path in the cache directory to the file in markdown format."
        ),
    ]
    json_file: Annotated[
        str,
        Field(
            description="The path in the cache directory to the file in JSON format."
        ),
    ]