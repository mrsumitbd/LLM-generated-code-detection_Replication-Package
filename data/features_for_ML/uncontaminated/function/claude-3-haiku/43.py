import requests
from tqdm import tqdm
from pathlib import Path

def download(src: str, dest: StrPath) -> None:
    """Simple request.get call with a progress bar
    Args:
        src: URL to be retrieved
        dest: Local destination path
    """
    response = requests.get(src, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024

    dest_path = Path(dest)
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    with open(dest, 'wb') as file, tqdm(total=total_size, unit='iB', unit_scale=True) as progress_bar:
        for chunk in response.iter_content(chunk_size=block_size):
            if chunk:
                file.write(chunk)
                progress_bar.update(len(chunk))