from llama_index.core.base.response.schema import (
    RESPONSE_TYPE,
    Response,
)
from typing import Annotated, Any
from mcp.shared.exceptions import McpError
from mcp.types import INTERNAL_ERROR, ErrorData, ToolAnnotations
from pydantic import Field
from docling_mcp.tools.llama_index._shared import (
    local_index_cache,
    milvus_vector_store,
    node_parser,
)

def search_documents(
    query: Annotated[
        str,
        Field(
            description="The search query text used to find relevant information in the indexed documents."
        ),
    ],
) -> SearchDocumentOutput:
    """Searches through previously uploaded and indexed documents using semantic search.

    This function retrieves relevant information from documents that have been processed
    and added to the vector database. It uses semantic similarity to find content that
    best matches the query, rather than simple keyword matching.
    """
    index = local_index_cache["milvus_index"]

    query_engine = index.as_query_engine()
    response: RESPONSE_TYPE = query_engine.query(query)

    if isinstance(response, Response):
        if response.response is not None:
            return SearchDocumentOutput(answer=response.response)
        else:
            raise McpError(
                ErrorData(
                    code=INTERNAL_ERROR,
                    message="Response object has no response content",
                )
            )
    else:
        raise McpError(
            ErrorData(
                code=INTERNAL_ERROR,
                message=f"Unexpected response type: {type(response)}",
            )
        )