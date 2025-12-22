import os
import re
import shutil
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple
from functools import wraps
import requests
from xml.etree import ElementTree as ET


def retry(exceptions):
    """Decorator to retry a function on specified exceptions."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries - 1:
                        raise
                    continue
        return wrapper
    return decorator


class DocumentProcessingToolkit:
    r"""A class representing a toolkit for processing document and return the content of the document.

    This class provides method for processing docx, pdf, pptx, etc. It cannot process excel files.
    """

    def __init__(self, cache_dir: Optional[str] = None):
        if cache_dir is None:
            self.cache_dir = tempfile.gettempdir()
        else:
            self.cache_dir = cache_dir
            os.makedirs(self.cache_dir, exist_ok=True)

    @retry((requests.RequestException,))
    def extract_document_content(self, document_path: str) -> Tuple[bool, str]:
        try:
            if self._is_webpage(document_path):
                file_path = self._download_file(document_path)
            else:
                file_path = document_path

            if not os.path.exists(file_path):
                return False, f"File not found: {file_path}"

            file_ext = Path(file_path).suffix.lower()

            if file_ext == '.pdf':
                content = self._extract_pdf_content(file_path)
            elif file_ext == '.docx':
                content = self._extract_docx_content(file_path)
            elif file_ext == '.pptx':
                content = self._extract_pptx_content(file_path)
            elif file_ext == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            else:
                return False, f"Unsupported file format: {file_ext}"

            if self._is_webpage(document_path):
                os.remove(file_path)

            return True, content

        except Exception as e:
            return False, f"Error processing document: {str(e)}"

    def _is_webpage(self, url: str) -> bool:
        return url.startswith('http://') or url.startswith('https://')

    def _download_file(self, url: str) -> str:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        content_disposition = response.headers.get('content-disposition', '')
        filename = re.findall(r'filename=([^;]+)', content_disposition)
        if filename:
            filename = filename[0].strip('"\'')
        else:
            filename = url.split('/')[-1].split('?')[0] or 'downloaded_file'

        file_path = os.path.join(self.cache_dir, filename)

        with open(file_path, 'wb') as f:
            f.write(response.content)

        return file_path

    def _get_formatted_time(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _unzip_file(self, zip_path: str) -> List[str]:
        extract_dir = os.path.join(self.cache_dir, f"unzip_{datetime.now().timestamp()}")
        os.makedirs(extract_dir, exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        extracted_files = []
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                extracted_files.append(os.path.join(root, file))

        return extracted_files

    def _extract_pdf_content(self, file_path: str) -> str:
        try:
            import PyPDF2
            content = []
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    content.append(page.extract_text())
            return '\n'.join(content)
        except ImportError:
            return "PyPDF2 not installed"

    def _extract_docx_content(self, file_path: str) -> str:
        extracted_files = self._unzip_file(file_path)
        document_xml = None

        for file in extracted_files:
            if file.endswith('document.xml'):
                document_xml = file
                break

        if not document_xml:
            return ""

        tree = ET.parse(document_xml)
        root = tree.getroot()

        namespaces = {
            'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
        }

        content = []
        for paragraph in root.findall('.//w:p', namespaces):
            para_text = []
            for text_elem in paragraph.findall('.//w:t', namespaces):
                if text_elem.text:
                    para_text.append(text_elem.text)
            if para_text:
                content.append(''.join(para_text))

        extract_dir = os.path.dirname(document_xml)
        shutil.rmtree(extract_dir, ignore_errors=True)

        return '\n'.join(content)

    def _extract_pptx_content(self, file_path: str) -> str:
        extracted_files = self._unzip_file(file_path)
        slide_files = [f for f in extracted_files if f.endswith('.xml') and '/slides/slide' in f]
        slide_files.sort()

        namespaces = {
            'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
            'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
            'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
        }

        content = []
        for slide_file in slide_files:
            tree = ET.parse(slide_file)
            root = tree.getroot()

            for text_elem in root.findall('.//a:t', namespaces):
                if text_elem.text:
                    content.append(text_elem.text)

        extract_dir = os.path.dirname(slide_files[0]) if slide_files else None
        if extract_dir:
            shutil.rmtree(os.path.dirname(extract_dir), ignore_errors=True)

        return '\n'.join(content)