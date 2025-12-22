import anthropic
import base64
import json
import os
from pathlib import Path


def build_roboflow(image_set, args, resolution):
    """
    Build a Roboflow dataset using Claude's vision capabilities.
    
    Args:
        image_set: List of image paths or image data
        args: Arguments containing model, max_tokens, and other settings
        resolution: Resolution setting for image processing
    
    Returns:
        Dictionary containing the built Roboflow dataset information
    """
    client = anthropic.Anthropic()
    
    # Process images and prepare them for Claude
    processed_images = []
    
    if isinstance(image_set, list):
        for image_item in image_set:
            if isinstance(image_item, str):
                # Handle file path
                if os.path.isfile(image_item):
                    with open(image_item, "rb") as f:
                        image_data = base64.standard_b64encode(f.read()).decode("utf-8")
                    # Determine media type from file extension
                    ext = Path(image_item).suffix.lower()
                    media_type_map = {
                        ".jpg": "image/jpeg",
                        ".jpeg": "image/jpeg",
                        ".png": "image/png",
                        ".gif": "image/gif",
                        ".webp": "image/webp"
                    }
                    media_type = media_type_map.get(ext, "image/jpeg")
                    processed_images.append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data
                        }
                    })
            elif isinstance(image_item, dict) and "data" in image_item:
                # Handle pre-encoded image data
                processed_images.append(image_item)
    
    # Build the message content
    content = [
        {
            "type": "text",
            "text": """Analyze these images and provide a Roboflow dataset structure. 
            For each image, identify:
            1. Objects/classes present
            2. Bounding box coordinates (normalized 0-1)
            3. Confidence scores
            4. Image metadata
            
            Return the response as a JSON object with the following structure:
            {
                "dataset_info": {
                    "name": "dataset_name",
                    "version": 1,
                    "classes": ["class1", "class2", ...],
                    "total_images": number
                },
                "images": [
                    {
                        "id": "image_id",
                        "filename": "filename",
                        "width": width,
                        "height": height,
                        "annotations": [
                            {
                                "class": "class_name",
                                "x": x_center,
                                "y": y_center,
                                "width": bbox_width,
                                "height": bbox_height,
                                "confidence": confidence_score
                            }
                        ]
                    }
                ]
            }"""
        }
    ]
    
    # Add processed images to content
    content.extend(processed_images)
    
    # Call Claude API with vision capabilities
    model = getattr(args, 'model', 'claude-3-5-sonnet-20241022')
    max_tokens = getattr(args, 'max_tokens', 4096)
    
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[
            {
                "role": "user",
                "content": content
            }
        ]
    )
    
    # Parse the response
    response_text = message.content[0].text
    
    # Extract JSON from the response
    try:
        # Try to find JSON in the response
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        if start_idx != -1 and end_idx > start_idx:
            json_str = response_text[start_idx:end_idx]
            roboflow_data = json.loads(json_str)
        else:
            # If no JSON found, create a basic structure
            roboflow_data = {
                "dataset_info": {
                    "name": "roboflow_dataset",
                    "version": 1,
                    "classes": [],
                    "total_images": len(image_set) if isinstance(image_set, list) else 1
                },
                "images": [],
                "raw_response": response_text
            }
    except json.JSONDecodeError:
        roboflow_data = {
            "dataset_info": {
                "name": "roboflow_dataset",
                "version": 1,
                "classes": [],
                "total_images": len(image_set) if isinstance(image_set, list) else 1
            },
            "images": [],
            "raw_response": response_text
        }
    
    # Add metadata
    roboflow_data["metadata"] = {
        "resolution": resolution,
        "model_used": model,
        "processing_complete": True
    }
    
    return roboflow_data