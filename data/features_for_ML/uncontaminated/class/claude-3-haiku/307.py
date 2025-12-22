import os
import zipfile
import requests
from datetime import datetime
from typing import Optional, Tuple, List
from functools import wraps

class DocumentProcessingToolkit:
    r"""A class representing a toolkit for processing document and return the content of the document.

    This class provides method for processing docx, pdf, pptx, etc. It cannot process excel files.
    """

    def __init__(self, cache_dir: Optional[str] = None):
        self.cache_dir = cache_dir or os.path.join(os.getcwd(), 'cache')
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    @retry((requests.RequestException))
    def extract_document_content(self, document_path: str) -> Tuple[bool, str]:
        if self._is_webpage(document_path):
            self._download_file(document_path)
            document_path = os.path.join(self.cache_dir, self._get_formatted_time() + os.path.splitext(document_path)[1])

        if document_path.endswith('.docx'):
            # Extract content from docx file
            return True, 'Docx content'
        elif document_path.endswith('.pdf'):
            # Extract content from pdf file
            return True, 'PDF content'
        elif document_path.endswith('.pptx'):
            # Extract content from pptx file
            return True, 'PPTX content'
        else:
            return False, 'Unsupported file type'

    def _is_webpage(self, url: str) -> bool:
        try:
            response = requests.head(url)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def _download_file(self, url: str):
        try:
            response = requests.get(url)
            file_path = os.path.join(self.cache_dir, self._get_formatted_time() + os.path.splitext(url)[1])
            with open(file_path, 'wb') as file:
                file.write(response.content)
        except requests.RequestException:
            pass

    def _get_formatted_time(self) -> str:
        return datetime.now().strftime('%Y%m%d_%H%M%S')

    def _unzip_file(self, zip_path: str) -> List[str]:
        extracted_files = []
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.cache_dir)
            extracted_files = [os.path.join(self.cache_dir, name) for name in zip_ref.namelist()]
        return extracted_files

def retry(exceptions, max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    retries += 1
                    if retries < max_retries:
                        print(f"Retrying {func.__name__} ({retries}/{max_retries})")
                        time.sleep(delay)
                    else:
                        raise
        return wrapper
    return decorator