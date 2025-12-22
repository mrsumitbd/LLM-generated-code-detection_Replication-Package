import os
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from PIL import Image
except ImportError:
    Image = None  # Pillow is optional; image loading will fail if not available


def _is_image_file(path: Path) -> bool:
    """Return True if the file has a common image extension."""
    return path.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"}


def _load_image(path: Path) -> Optional[Any]:
    """Load an image using Pillow if available."""
    if Image is None:
        return None
    try:
        return Image.open(path).convert("RGB")
    except Exception:
        return None


def process_single_directory(basedir: str, episode_dir: str, load_image: bool) -> Optional[Dict[str, Any]]:
    """
    Process a single episode directory.

    Parameters
    ----------
    basedir : str
        The base directory containing all episode directories.
    episode_dir : str
        The relative path (from basedir) to the episode directory to process.
    load_image : bool
        If True, load image data into memory; otherwise, only return file paths.

    Returns
    -------
    Optional[Dict[str, Any]]
        A dictionary with keys:
            - 'episode': the episode directory name
            - 'metadata': a dict loaded from a JSON file if present
            - 'images': a list of image data (PIL.Image objects) or file paths
        Returns None if the episode directory does not exist or contains no image files.
    """
    # Resolve absolute path
    episode_path = Path(basedir) / episode_dir
    if not episode_path.is_dir():
        return None

    # Gather image files
    image_files: List[Path] = []
    for root, _, files in os.walk(episode_path):
        for f in files:
            p = Path(root) / f
            if _is_image_file(p):
                image_files.append(p)

    if not image_files:
        return None

    # Load metadata if present
    metadata: Dict[str, Any] | None = None
    meta_path = episode_path / "metadata.json"
    if meta_path.is_file():
        try:
            with meta_path.open("r", encoding="utf-8") as fp:
                metadata = json.load(fp)
        except Exception:
            metadata = None

    # Load images or return paths
    if load_image:
        images: List[Any] = []
        for img_path in image_files:
            img = _load_image(img_path)
            if img is not None:
                images.append(img)
        # If no images could be loaded, return None
        if not images:
            return None
    else:
        images = [str(p) for p in image_files]

    return {
        "episode": episode_dir,
        "metadata": metadata,
        "images": images,
    }