import anthropic
import json
import base64
from pathlib import Path


class StableAnimatorSkeletonNode:
    """
    StableAnimator生成视频POSE骨架
    """

    def __init__(self):
        self.client = anthropic.Anthropic()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "prompt": ("STRING", {"default": "Extract the skeleton pose from this image"}),
            },
            "optional": {
                "model": ("STRING", {"default": "claude-3-5-sonnet-20241022"}),
            },
        }

    def extraction(self, **kwargs):
        image = kwargs.get("image")
        prompt = kwargs.get("prompt", "Extract the skeleton pose from this image")
        model = kwargs.get("model", "claude-3-5-sonnet-20241022")

        if image is None:
            raise ValueError("Image input is required")

        # Convert image tensor to base64
        import numpy as np

        if isinstance(image, np.ndarray):
            # Normalize to 0-255 range if needed
            if image.dtype == np.float32 or image.dtype == np.float64:
                if image.max() <= 1.0:
                    image = (image * 255).astype(np.uint8)
                else:
                    image = image.astype(np.uint8)
            else:
                image = image.astype(np.uint8)

            # Handle different image shapes
            if len(image.shape) == 3:
                if image.shape[2] == 4:  # RGBA
                    from PIL import Image

                    pil_image = Image.fromarray(image, "RGBA")
                elif image.shape[2] == 3:  # RGB
                    from PIL import Image

                    pil_image = Image.fromarray(image, "RGB")
                else:
                    raise ValueError(f"Unsupported image shape: {image.shape}")
            else:
                raise ValueError(f"Unsupported image shape: {image.shape}")

            # Convert PIL image to base64
            import io

            buffer = io.BytesIO()
            pil_image.save(buffer, format="PNG")
            image_data = base64.standard_b64encode(buffer.getvalue()).decode("utf-8")
        else:
            raise ValueError("Image must be a numpy array")

        # Call Claude API with vision capability
        message = self.client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": prompt
                            + "\n\nPlease provide the skeleton pose data in JSON format with the following structure:\n"
                            + '{"keypoints": [{"name": "joint_name", "x": x_coord, "y": y_coord, "confidence": confidence_score}], '
                            + '"skeleton": [[joint1_idx, joint2_idx], ...]}',
                        },
                    ],
                }
            ],
        )

        # Parse the response
        response_text = message.content[0].text

        # Extract JSON from response
        try:
            # Try to find JSON in the response
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                skeleton_data = json.loads(json_str)
            else:
                # If no JSON found, create a default structure
                skeleton_data = {
                    "keypoints": [],
                    "skeleton": [],
                    "raw_response": response_text,
                }
        except json.JSONDecodeError:
            skeleton_data = {
                "keypoints": [],
                "skeleton": [],
                "raw_response": response_text,
            }

        return (skeleton_data,)


NODE_CLASS_MAPPINGS = {"StableAnimatorSkeletonNode": StableAnimatorSkeletonNode}
NODE_DISPLAY_NAME_MAPPINGS = {
    "StableAnimatorSkeletonNode": "StableAnimator Skeleton Extraction"
}