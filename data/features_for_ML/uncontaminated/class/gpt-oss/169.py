import os
import shutil

class BaseImageUploader:
    """
    A simple image uploader that copies the given file to a local 'uploads' directory.
    """

    def __init__(self, upload_dir: str = "uploads"):
        """
        Initialize the uploader.

        :param upload_dir: Directory where uploaded files will be stored.
        """
        self.upload_dir = os.path.abspath(upload_dir)
        os.makedirs(self.upload_dir, exist_ok=True)

    def upload_file(self, filename: str) -> str:
        """
        Copy the specified file to the upload directory.

        :param filename: Path to the file to upload.
        :return: Absolute path to the uploaded file.
        :raises FileNotFoundError: If the source file does not exist.
        :raises IOError: If the file cannot be copied.
        """
        src_path = os.path.abspath(filename)

        if not os.path.isfile(src_path):
            raise FileNotFoundError(f"Source file not found: {src_path}")

        # Preserve the original filename
        dest_path = os.path.join(self.upload_dir, os.path.basename(src_path))

        # Copy the file
        shutil.copy2(src_path, dest_path)

        return dest_path