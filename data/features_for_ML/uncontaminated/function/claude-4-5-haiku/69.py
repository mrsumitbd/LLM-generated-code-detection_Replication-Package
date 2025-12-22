import anthropic
import base64
import os
from pathlib import Path


def check_input_image(input_image):
    """
    Check if an input image is valid and can be processed by Claude's vision API.
    
    Args:
        input_image: Path to an image file (string or Path object)
    
    Returns:
        dict: A dictionary containing:
            - 'valid': bool indicating if the image is valid
            - 'message': str with details about the validation
            - 'analysis': str with Claude's analysis of the image (if valid)
    """
    # Convert to Path object if string
    if isinstance(input_image, str):
        input_image = Path(input_image)
    
    # Check if file exists
    if not input_image.exists():
        return {
            'valid': False,
            'message': f"File does not exist: {input_image}",
            'analysis': None
        }
    
    # Check if it's a file
    if not input_image.is_file():
        return {
            'valid': False,
            'message': f"Path is not a file: {input_image}",
            'analysis': None
        }
    
    # Check file extension
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    if input_image.suffix.lower() not in valid_extensions:
        return {
            'valid': False,
            'message': f"Invalid file extension. Supported formats: {', '.join(valid_extensions)}",
            'analysis': None
        }
    
    # Check file size (Claude has limits, typically 20MB)
    file_size = input_image.stat().st_size
    max_size = 20 * 1024 * 1024  # 20MB
    if file_size > max_size:
        return {
            'valid': False,
            'message': f"File size ({file_size / 1024 / 1024:.2f}MB) exceeds maximum allowed size (20MB)",
            'analysis': None
        }
    
    # Try to read and encode the image
    try:
        with open(input_image, 'rb') as f:
            image_data = f.read()
        
        # Encode to base64
        base64_image = base64.standard_b64encode(image_data).decode('utf-8')
        
        # Determine media type
        extension = input_image.suffix.lower()
        media_type_map = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        media_type = media_type_map[extension]
        
        # Try to use Claude's vision API to analyze the image
        client = anthropic.Anthropic()
        
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": base64_image,
                            },
                        },
                        {
                            "type": "text",
                            "text": "Briefly describe what you see in this image in 1-2 sentences."
                        }
                    ],
                }
            ],
        )
        
        analysis = message.content[0].text
        
        return {
            'valid': True,
            'message': f"Image is valid and readable. File size: {file_size / 1024:.2f}KB",
            'analysis': analysis
        }
        
    except FileNotFoundError:
        return {
            'valid': False,
            'message': f"Could not read file: {input_image}",
            'analysis': None
        }
    except IOError as e:
        return {
            'valid': False,
            'message': f"IO error reading file: {str(e)}",
            'analysis': None
        }
    except anthropic.APIError as e:
        return {
            'valid': False,
            'message': f"API error processing image: {str(e)}",
            'analysis': None
        }
    except Exception as e:
        return {
            'valid': False,
            'message': f"Error processing image: {str(e)}",
            'analysis': None
        }


if __name__ == "__main__":
    # Test with a sample image
    import sys
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        result = check_input_image(image_path)
        print(f"Valid: {result['valid']}")
        print(f"Message: {result['message']}")
        if result['analysis']:
            print(f"Analysis: {result['analysis']}")
    else:
        print("Usage: python solution.py <image_path>")