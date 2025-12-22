from typing import Optional, Dict, Any
import os
import shutil
import logging

def process_single_directory(basedir: str, episode_dir: str, load_image: bool) -> Optional[Dict[str, Any]]:
    try:
        episode_path = os.path.join(basedir, episode_dir)
        if not os.path.isdir(episode_path):
            logging.warning(f"Skipping non-directory: {episode_path}")
            return None

        episode_data = {
            "episode_dir": episode_dir,
            "image_path": None
        }

        if load_image:
            image_path = os.path.join(episode_path, "cover.jpg")
            if os.path.isfile(image_path):
                episode_data["image_path"] = image_path
            else:
                logging.warning(f"No cover.jpg found in {episode_path}")

        return episode_data
    except Exception as e:
        logging.error(f"Error processing directory {episode_dir}: {e}")
        return None