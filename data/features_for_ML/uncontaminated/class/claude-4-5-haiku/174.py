import anthropic
import base64
import json
import os
from pathlib import Path


class FastModeRunner:

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"

    def run(self, frames_guide, frames_style, batch_size, window_size, ebsynth_config, save_path=None):
        """
        Run fast mode processing using Claude's vision capabilities.
        
        Args:
            frames_guide: List of guide frame paths
            frames_style: List of style frame paths
            batch_size: Number of frames to process in each batch
            window_size: Size of the processing window
            ebsynth_config: Configuration for ebsynth processing
            save_path: Optional path to save results
            
        Returns:
            Dictionary containing processing results
        """
        results = {
            "processed_frames": [],
            "metadata": {
                "batch_size": batch_size,
                "window_size": window_size,
                "total_frames": len(frames_guide),
                "ebsynth_config": ebsynth_config
            }
        }
        
        # Process frames in batches
        for batch_idx in range(0, len(frames_guide), batch_size):
            batch_end = min(batch_idx + batch_size, len(frames_guide))
            batch_guide_frames = frames_guide[batch_idx:batch_end]
            batch_style_frames = frames_style[batch_idx:batch_end]
            
            # Prepare image data for Claude
            guide_images = []
            style_images = []
            
            for frame_path in batch_guide_frames:
                if os.path.exists(frame_path):
                    with open(frame_path, "rb") as f:
                        image_data = base64.standard_b64encode(f.read()).decode("utf-8")
                        guide_images.append({
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_data
                            }
                        })
            
            for frame_path in batch_style_frames:
                if os.path.exists(frame_path):
                    with open(frame_path, "rb") as f:
                        image_data = base64.standard_b64encode(f.read()).decode("utf-8")
                        style_images.append({
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_data
                            }
                        })
            
            # Build the message content
            content = []
            
            # Add guide images
            if guide_images:
                content.append({
                    "type": "text",
                    "text": f"Guide frames for batch {batch_idx // batch_size + 1}:"
                })
                content.extend(guide_images)
            
            # Add style images
            if style_images:
                content.append({
                    "type": "text",
                    "text": f"Style frames for batch {batch_idx // batch_size + 1}:"
                })
                content.extend(style_images)
            
            # Add processing instructions
            content.append({
                "type": "text",
                "text": f"""Analyze these guide and style frames for fast mode processing.
                
Configuration:
- Batch size: {batch_size}
- Window size: {window_size}
- EBSynth config: {json.dumps(ebsynth_config)}

Please provide:
1. Analysis of the guide frames' motion and structure
2. Analysis of the style frames' visual characteristics
3. Recommendations for frame interpolation
4. Suggested processing parameters for optimal results

Format your response as JSON with keys: motion_analysis, style_analysis, interpolation_recommendations, processing_parameters"""
            })
            
            # Call Claude API
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": content
                    }
                ]
            )
            
            # Parse response
            response_text = message.content[0].text
            
            # Try to extract JSON from response
            try:
                # Find JSON in response
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    batch_analysis = json.loads(json_str)
                else:
                    batch_analysis = {"raw_analysis": response_text}
            except json.JSONDecodeError:
                batch_analysis = {"raw_analysis": response_text}
            
            # Store batch results
            batch_result = {
                "batch_index": batch_idx // batch_size,
                "frame_range": f"{batch_idx}-{batch_end-1}",
                "analysis": batch_analysis,
                "frame_count": len(batch_guide_frames)
            }
            
            results["processed_frames"].append(batch_result)
        
        # Save results if path provided
        if save_path:
            os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
            with open(save_path, "w") as f:
                json.dump(results, f, indent=2)
        
        return results