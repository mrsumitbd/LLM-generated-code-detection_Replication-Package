import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Generator, MutableMapping, Optional, Union
from http.cookiejar import CookieJar

def aria2c(
    urls: Union[str, list[str], dict[str, Any], list[dict[str, Any]]],
    output_dir: Path,
    filename: str,
    headers: Optional[MutableMapping[str, Union[str, bytes]]] = None,
    cookies: Optional[Union[MutableMapping[str, str], CookieJar]] = None,
    proxy: Optional[str] = None,
    max_workers: Optional[int] = None,
) -> Generator[dict[str, Any], None, None]:
    """
    Download files using Aria2(c).
    https://aria2.github.io

    Yields the following download status updates while chunks are downloading:

    - {total: 100} (100% download total)
    - {completed: 1} (1% download progress out of 100%)
    - {downloaded: "10.1 MB/s"} (currently downloading at a rate of 10.1 MB/s)

    The data is in the same format accepted by rich's progress.update() function.

    Parameters:
        urls: Web URL(s) to file(s) to download. You can use a dictionary with the key
            "url" for the URI, and other keys for extra arguments to use per-URL.
        output_dir: The folder to save the file into. If the save path's directory does
            not exist then it will be made automatically.
        filename: The filename or filename template to use for each file. The variables
            you can use are `i` for the URL index and `ext` for the URL extension.
        headers: A mapping of HTTP Header Key/Values to use for all downloads.
        cookies: A mapping of Cookie Key/Values or a Cookie Jar to use for all downloads.
        proxy: An optional proxy URI to route connections through for all downloads.
        max_workers: The maximum amount of threads to use for downloads. Defaults to
            min(32,(cpu_count+4)). Use for the --max-concurrent-downloads option.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    if isinstance(urls, str):
        urls = [urls]
    elif isinstance(urls, dict):
        urls = [urls]

    for i, url_info in enumerate(urls):
        if isinstance(url_info, dict):
            url = url_info["url"]
        else:
            url = url_info

        ext = os.path.splitext(url)[1]
        save_path = output_dir / filename.format(i=i, ext=ext)

        aria2_cmd = ["aria2c", url, f"--out={save_path.name}"]

        if headers:
            for header, value in headers.items():
                aria2_cmd.append(f"--header={header}:{value}")

        if cookies:
            if isinstance(cookies, MutableMapping):
                for key, value in cookies.items():
                    aria2_cmd.append(f"--cookie={key}={value}")
            elif isinstance(cookies, CookieJar):
                for cookie in cookies:
                    aria2_cmd.append(f"--cookie={cookie.name}={cookie.value}")

        if proxy:
            aria2_cmd.append(f"--all-proxy={proxy}")

        if max_workers:
            aria2_cmd.append(f"--max-concurrent-downloads={max_workers}")

        process = subprocess.Popen(aria2_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        total = 0
        completed = 0
        downloaded = "0 B/s"

        while True:
            line = process.stdout.readline().decode().strip()
            if not line:
                break

            if line.startswith("Download complete:"):
                yield {"total": 100}
                yield {"completed": 100}
                yield {"downloaded": "0 B/s"}
                break

            if "%" in line:
                parts = line.split()
                total = int(parts[1][:-1])
                completed = int(parts[0][:-1])
                downloaded = parts[3]
                yield {"total": total}
                yield {"completed": completed}
                yield {"downloaded": downloaded}

        retcode = process.wait()
        if retcode != 0:
            stderr = process.stderr.read().decode().strip()
            raise subprocess.CalledProcessError(retcode, aria2_cmd, stderr)

        shutil.move(save_path, output_dir)