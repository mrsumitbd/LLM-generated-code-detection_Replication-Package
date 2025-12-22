def download(src: str, dest: StrPath) -> None:
    """Simple request.get call with a progress bar
    Args:
        src: URL to be retrieved
        dest: Local destination path
    """
    import requests
    from pathlib import Path
    
    response = requests.get(src, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    
    dest_path = Path(dest)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    downloaded = 0
    with open(dest_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    progress = (downloaded / total_size) * 100
                    print(f'\rProgress: {progress:.1f}%', end='', flush=True)
    
    if total_size > 0:
        print()