from typing import Optional, Tuple, List
import requests
from retry import retry
import zipfile
import os
import textract

class DocumentProcessingToolkit:
    r"""A class representing a toolkit for processing document and return the content of the document.

    This class provides method for processing docx, pdf, pptx, etc. It cannot process excel files.
    """

    def __init__(self, cache_dir: Optional[str] = None):
        self.cache_dir = cache_dir

    @retry((requests.RequestException))
    def extract_document_content(self, document_path: str) -> Tuple[bool, str]:
        if self._is_webpage(document_path):
            self._download_file(document_path)
            document_path = os.path.join(self.cache_dir, os.path.basename(document_path))
        if document_path.endswith('.zip'):
            extracted_files = self._unzip_file(document_path)
            content = ''
            for file in extracted_files:
                content += textract.process(file).decode('utf-8', errors='ignore') + '\n'
            return True, content
        else:
            return True, textract.process(document_path).decode('utf-8', errors='ignore')

    def _is_webpage(self, url: str) -> bool:
        return url.startswith('http') or url.startswith('www')

    def _download_file(self, url: str):
        response = requests.get(url)
        with open(os.path.join(self.cache_dir, os.path.basename(url)), 'wb') as file:
            file.write(response.content)

    def _get_formatted_time(self) -> str:
        pass

    def _unzip_file(self, zip_path: str) -> List[str]:
        extracted_files = []
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.cache_dir)
            extracted_files = [os.path.join(self.cache_dir, file) for file in zip_ref.namelist()]
        return extracted_files