import anthropic
import base64
import os
from pathlib import Path


class BaseImageUploader:

    def upload_file(self, filename):
        """
        Upload an image file and return the media_id for use in Claude API calls.
        
        Args:
            filename: Path to the image file to upload
            
        Returns:
            The media_id of the uploaded file
        """
        # Read the image file
        file_path = Path(filename)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {filename}")
        
        # Determine the media type based on file extension
        extension = file_path.suffix.lower()
        media_type_map = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        
        if extension not in media_type_map:
            raise ValueError(f"Unsupported image format: {extension}")
        
        media_type = media_type_map[extension]
        
        # Read and encode the image file
        with open(file_path, 'rb') as f:
            image_data = base64.standard_b64encode(f.read()).decode('utf-8')
        
        # Initialize the Anthropic client
        client = anthropic.Anthropic()
        
        # Upload the file using the Files API
        with open(file_path, 'rb') as f:
            response = client.beta.files.upload(
                file=(file_path.name, f, media_type),
            )
        
        # Return the media_id from the response
        return response.id