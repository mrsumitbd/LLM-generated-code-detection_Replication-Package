def process_single_directory(basedir: str, episode_dir: str, load_image: bool) -> Optional[Dict[str, Any]]:
    import os
    import json
    from pathlib import Path
    
    episode_path = os.path.join(basedir, episode_dir)
    
    if not os.path.isdir(episode_path):
        return None
    
    metadata_file = os.path.join(episode_path, 'metadata.json')
    if not os.path.exists(metadata_file):
        return None
    
    try:
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
    except (json.JSONDecodeError, IOError):
        return None
    
    result = {
        'episode_dir': episode_dir,
        'metadata': metadata,
        'image': None
    }
    
    if load_image:
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
        image_file = None
        
        for ext in image_extensions:
            potential_image = os.path.join(episode_path, f'image{ext}')
            if os.path.exists(potential_image):
                image_file = potential_image
                break
        
        if image_file is None:
            for file in os.listdir(episode_path):
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    image_file = os.path.join(episode_path, file)
                    break
        
        if image_file:
            try:
                from PIL import Image
                image = Image.open(image_file)
                result['image'] = image
            except Exception:
                result['image'] = None
    
    return result