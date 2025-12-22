import os
import urllib.request
import urllib.error

def http_get(url, path):
    """
    Downloads a URL to a given path on disc.
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    try:
        with urllib.request.urlopen(url) as response, open(path, 'wb') as out_file:
            # Read in chunks to avoid loading entire file into memory
            chunk_size = 8192
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                out_file.write(chunk)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP error {e.code} while downloading {url}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"URL error while downloading {url}: {e.reason}") from e
    except OSError as e:
        raise RuntimeError(f"File error while writing to {path}: {e.strerror}") from e