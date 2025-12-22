import os
from pathlib import Path
from typing import Union

import requests
from tqdm import tqdm

# StrPath is typically defined elsewhere in the project; we accept str or Path here.
StrPath = Union[str, Path]


def download(src: str, dest: StrPath) -> None:
    """Simple request.get call with a progress bar

    Args:
        src: URL to be retrieved
        dest: Local destination path
    """
    dest_path = Path(dest)
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    with requests.get(src, stream=True) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        chunk_size = 1024 * 1024  # 1 MB

        with open(dest_path, "wb") as f, tqdm(
            total=total,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            desc=f"Downloading {src}",
            initial=0,
            ascii=True,
        ) as bar:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))