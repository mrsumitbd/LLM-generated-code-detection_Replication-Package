from typing import Any, Literal, Protocol, TypeVar, cast
from nutrient_dws.types.build_output import (
    HTMLOutput,
    ImageOutput,
    ImageOutputOptions,
    JSONContentOutput,
    JSONContentOutputOptions,
    MarkdownOutput,
    OfficeOutput,
    PDFAOutput,
    PDFAOutputOptions,
    PDFOutput,
    PDFOutputOptions,
    PDFUAOutput,
    PDFUAOutputOptions,
)

def html(layout: Literal["page", "reflow"]) -> HTMLOutput:
        """HTML output configuration.

        Args:
            layout: The layout type to use for conversion to HTML

        Returns:
            HTMLOutput object
        """
        return {
            "type": "html",
            "layout": layout,
        }