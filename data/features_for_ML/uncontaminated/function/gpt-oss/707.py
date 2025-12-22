import os
import csv
import shutil
from pathlib import Path
from typing import Iterable, Tuple, List, Dict, Any, Union

try:
    from PIL import Image
except ImportError:
    Image = None  # PIL is optional; resizing will be skipped if unavailable


def build_roboflow(
    image_set: Iterable[Union[str, Tuple[str, List[Dict[str, Any]]]]],
    args: Any,
    resolution: Tuple[int, int] = None,
) -> str:
    """
    Build a Roboflow-compatible dataset directory from a collection of images
    (and optional annotations).

    Parameters
    ----------
    image_set : iterable
        An iterable of either image file paths (str) or tuples of the form
        (image_path, annotations).  Each annotation is expected to be a dict
        with at least the keys: 'class' and 'bbox', where 'bbox' is a
        tuple/list of (xmin, ymin, xmax, ymax).
    args : object
        Namespace or object containing optional attributes:
            - dataset_name (default: 'dataset')
            - roboflow_project (default: None)
            - roboflow_version (default: None)
            - roboflow_api_key (default: None)
            - roboflow_workspace (default: None)
    resolution : tuple of int, optional
        Target (width, height) to resize images to.  If None, original size
        is preserved.

    Returns
    -------
    str
        Path to the created dataset directory.
    """
    # Determine dataset name and output directory
    dataset_name = getattr(args, "dataset_name", "dataset")
    base_dir = Path.cwd() / dataset_name / "roboflow"
    base_dir.mkdir(parents=True, exist_ok=True)

    # Prepare annotations CSV
    annotations_path = base_dir / "annotations.csv"
    csv_header = ["filename", "width", "height", "class", "xmin", "ymin", "xmax", "ymax"]
    with annotations_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_header)
        writer.writeheader()

        for item in image_set:
            # Determine if item includes annotations
            if isinstance(item, (tuple, list)) and len(item) == 2:
                img_path, ann_list = item
            else:
                img_path = item
                ann_list = []

            img_path = Path(img_path)
            if not img_path.is_file():
                # Skip missing files
                continue

            # Load image
            try:
                img = Image.open(img_path).convert("RGB")
            except Exception:
                # If PIL is unavailable or image cannot be opened, skip
                continue

            original_size = img.size  # (width, height)

            # Resize if requested
            if resolution and Image:
                img = img.resize(resolution, Image.ANTIALIAS)
                width, height = resolution
            else:
                width, height = original_size

            # Save processed image
            out_img_path = base_dir / img_path.name
            try:
                img.save(out_img_path, format="JPEG")
            except Exception:
                # If saving fails, skip this image
                continue

            # Write annotations
            for ann in ann_list:
                # Ensure required keys exist
                if "class" not in ann or "bbox" not in ann:
                    continue
                bbox = ann["bbox"]
                if (
                    not isinstance(bbox, (tuple, list))
                    or len(bbox) != 4
                    or not all(isinstance(v, (int, float)) for v in bbox)
                ):
                    continue
                xmin, ymin, xmax, ymax = bbox
                writer.writerow(
                    {
                        "filename": img_path.name,
                        "width": width,
                        "height": height,
                        "class": ann["class"],
                        "xmin": xmin,
                        "ymin": ymin,
                        "xmax": xmax,
                        "ymax": ymax,
                    }
                )

    return str(base_dir)