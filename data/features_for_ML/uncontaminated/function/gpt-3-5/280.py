from typing import Optional, Dict, Any

def process_single_directory(basedir: str, episode_dir: str, load_image: bool) -> Optional[Dict[str, Any]]:
    if load_image:
        # Load image processing code here
        return {"message": f"Processing images in {basedir}/{episode_dir}"}
    else:
        return {"message": f"Skipping image processing for {basedir}/{episode_dir}"}