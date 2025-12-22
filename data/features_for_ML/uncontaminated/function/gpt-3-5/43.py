def download(src: str, dest: StrPath) -> None:
    import requests
    from tqdm import tqdm
    response = requests.get(src, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    t = tqdm(total=total_size, unit='B', unit_scale=True)
    with open(dest, 'wb') as f:
        for data in response.iter_content(block_size):
            t.update(len(data))
            f.write(data)
    t.close()