import os
import requests
from tqdm import tqdm

def download(src: str, dest: StrPath) -> None:
    """Simple request.get call with a progress bar
    Args:
        src: URL to be retrieved
        dest: Local destination path
    """
    req = requests.get(src, stream=True)
    assert req.status_code == 200
    tsize = int(req.headers.get("content-length", 0))
    progress = tqdm(total=tsize, unit="iB", unit_scale=True, position=0, leave=False)

    with open(dest, "wb") as handle:
        progress.set_description(os.path.basename(dest))
        for chunk in req.iter_content(chunk_size=1024):
            handle.write(chunk)
            progress.update(len(chunk))