import pathlib
import mimetypes
from typing import Literal

def extract_simple(
    file_path: str,
    mime_type: str | None = None,
    response_format: Literal["text", "markdown"] = "text",
) -> str:
    """
    Extract plain text from a file. Supports a handful of common formats:
    - Plain text (.txt, .md)
    - PDF (.pdf) using PyPDF2
    - DOCX (.docx) using python-docx
    - HTML (.html, .htm) using BeautifulSoup

    Parameters
    ----------
    file_path : str
        Path to the file to extract from.
    mime_type : str | None, optional
        MIME type of the file. If None, it will be guessed from the file extension.
    response_format : Literal["text", "markdown"], optional
        If "markdown", the extracted text will be wrapped in a Markdown code block.

    Returns
    -------
    str
        The extracted text, optionally wrapped in Markdown.
    """
    path = pathlib.Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Determine MIME type if not provided
    if mime_type is None:
        mime_type, _ = mimetypes.guess_type(str(path))
        if mime_type is None:
            # Fallback: use file extension
            ext = path.suffix.lower()
            if ext in {".txt", ".md"}:
                mime_type = "text/plain"
            elif ext == ".pdf":
                mime_type = "application/pdf"
            elif ext == ".docx":
                mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            elif ext in {".html", ".htm"}:
                mime_type = "text/html"
            else:
                mime_type = "application/octet-stream"

    extracted = ""

    try:
        if mime_type in {"text/plain", "text/markdown"} or path.suffix.lower() in {".txt", ".md"}:
            extracted = path.read_text(encoding="utf-8", errors="ignore")

        elif mime_type == "application/pdf" or path.suffix.lower() == ".pdf":
            try:
                import PyPDF2
            except ImportError:
                raise ImportError("PyPDF2 is required for PDF extraction")
            with path.open("rb") as f:
                reader = PyPDF2.PdfReader(f)
                pages = []
                for page in reader.pages:
                    pages.append(page.extract_text() or "")
                extracted = "\n".join(pages)

        elif mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or path.suffix.lower() == ".docx":
            try:
                import docx
            except ImportError:
                raise ImportError("python-docx is required for DOCX extraction")
            doc = docx.Document(str(path))
            paragraphs = [para.text for para in doc.paragraphs]
            extracted = "\n".join(paragraphs)

        elif mime_type in {"text/html", "application/xhtml+xml"} or path.suffix.lower() in {".html", ".htm"}:
            try:
                from bs4 import BeautifulSoup
            except ImportError:
                raise ImportError("beautifulsoup4 is required for HTML extraction")
            html = path.read_text(encoding="utf-8", errors="ignore")
            soup = BeautifulSoup(html, "html.parser")
            extracted = soup.get_text(separator="\n", strip=True)

        else:
            # Unsupported format: try to read raw bytes and decode
            try:
                extracted = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                extracted = ""

    except Exception as exc:
        # In case of any error, return empty string
        extracted = ""

    if response_format == "markdown":
        return f"```text\n{extracted}\n```"
    return extracted