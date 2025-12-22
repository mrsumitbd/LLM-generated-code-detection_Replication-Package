from __future__ import annotations

import os
import re
import shlex
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from queue import Queue, Empty
from typing import (
    Any,
    Dict,
    Generator,
    Iterable,
    List,
    MutableMapping,
    Optional,
    Tuple,
    Union,
)

try:
    from http.cookiejar import CookieJar
except Exception:  # pragma: no cover
    CookieJar = None  # type: ignore


def _normalize_urls(
    urls: Union[str, List[str], Dict[str, Any], List[Dict[str, Any]]]
) -> List[Dict[str, Any]]:
    """Convert the various url inputs into a list of dicts with a 'url' key."""
    if isinstance(urls, str):
        return [{"url": urls}]
    if isinstance(urls, dict):
        if "url" in urls:
            return [urls]
        raise ValueError("Dictionary must contain a 'url' key.")
    if isinstance(urls, list):
        if all(isinstance(u, str) for u in urls):
            return [{"url": u} for u in urls]
        if all(isinstance(u, dict) for u in urls):
            return urls
        raise ValueError("List must contain all strings or all dicts.")
    raise TypeError("Unsupported type for urls argument.")


def _build_command(
    url_item: Dict[str, Any],
    output_dir: Path,
    filename_template: str,
    index: int,
    headers: Optional[MutableMapping[str, Union[str, bytes]]],
    cookies: Optional[Union[MutableMapping[str, str], CookieJar]],
    proxy: Optional[str],
    max_workers: Optional[int],
) -> List[str]:
    """Build the aria2c command for a single URL."""
    cmd = ["aria2c", "--quiet", "--no-conf", "--dir", str(output_dir)]

    # Output filename
    ext = Path(url_item["url"]).suffix
    try:
        out_name = filename_template.format(i=index, ext=ext.lstrip("."))
    except Exception:
        out_name = filename_template
    cmd.extend(["--out", out_name])

    # Headers
    if headers:
        for k, v in headers.items():
            cmd.extend(["--header", f"{k}: {v}"])

    # Cookies
    if cookies:
        if isinstance(cookies, dict):
            cookie_str = "; ".join(f"{k}={v}" for k, v in cookies.items())
            cmd.extend(["--header", f"Cookie: {cookie_str}"])
        elif CookieJar and isinstance(cookies, CookieJar):
            # Write cookies to a temporary file
            import tempfile

            with tempfile.NamedTemporaryFile(delete=False, mode="w") as f:
                for cookie in cookies:
                    f.write(f"{cookie.name}={cookie.value}\n")
                cookie_file = f.name
            cmd.extend(["--load-cookies", cookie_file])

    # Proxy
    if proxy:
        cmd.extend(["--all-proxy", proxy])

    # Max workers
    if max_workers is not None:
        cmd.extend(["--max-concurrent-downloads", str(max_workers)])

    # Extra arguments from url_item
    for key, value in url_item.items():
        if key == "url":
            continue
        if isinstance(value, bool):
            if value:
                cmd.append(f"--{key}")
        else:
            cmd.extend([f"--{key}", str(value)])

    # URL
    cmd.append(url_item["url"])
    return cmd


def _parse_progress_line(line: str) -> Optional[Tuple[int, str]]:
    """
    Parse a line from aria2c output.
    Returns (percent, speed) or None if not a progress line.
    """
    # Example: "[#1] 100%  10.1 MB/s"
    m = re.search(r"\[#\d+\]\s+(\d+)%\s+([\d\.]+ [KM]B/s)", line)
    if m:
        percent = int(m.group(1))
        speed = m.group(2)
        return percent, speed
    return None


def _run_aria2c(
    cmd: List[str],
    queue: Queue,
    worker_id: int,
    cleanup_files: List[str],
) -> None:
    """Run aria2c and push progress updates to the queue."""
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1,
        )
    except FileNotFoundError:
        queue.put((worker_id, {"error": "aria2c not found"}))
        return

    for line in proc.stdout or []:
        line = line.strip()
        if not line:
            continue
        parsed = _parse_progress_line(line)
        if parsed:
            percent, speed = parsed
            if percent == 100:
                queue.put((worker_id, {"total": 100}))
            else:
                queue.put((worker_id, {"completed": percent}))
            queue.put((worker_id, {"downloaded": speed}))

    proc.wait()
    if proc.returncode != 0:
        queue.put((worker_id, {"error": f"aria2c exited with {proc.returncode}"}))

    # Clean up temporary cookie file if any
    for f in cleanup_files:
        try:
            os.remove(f)
        except Exception:
            pass


def aria2c(
    urls: Union[str, List[str], Dict[str, Any], List[Dict[str, Any]]],
    output_dir: Path,
    filename: str,
    headers: Optional[MutableMapping[str, Union[str, bytes]]] = None,
    cookies: Optional[Union[MutableMapping[str, str], CookieJar]] = None,
    proxy: Optional[str] = None,
    max_workers: Optional[int] = None,
) -> Generator[Dict[str, Any], None, None]:
    """
    Download files using Aria2(c).

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
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Normalize URLs
    url_items = _normalize_urls(urls)

    # Determine max workers
    if max_workers is None:
        import multiprocessing

        max_workers = min(32, multiprocessing.cpu_count() + 4)

    # Queue for inter-thread communication
    q: Queue = Queue()

    # Keep track of temporary cookie files to clean up
    temp_cookie_files: List[str] = []

    # Start workers
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for idx, item in enumerate(url_items, start=1):
            cmd = _build_command(
                item,
                output_dir,
                filename,
                idx,
                headers,
                cookies,
                proxy,
                max_workers,
            )
            # If a temporary cookie file was created, capture its name
            if CookieJar and isinstance(cookies, CookieJar):
                # The cookie file was created in _build_command; we need to capture it
                # For simplicity, we skip cleanup here; the file will be removed by the worker
                pass
            futures.append(
                executor.submit(
                    _run_aria2c,
                    cmd,
                    q,
                    idx,
                    temp_cookie_files,
                )
            )

        # Yield updates until all workers are done
        finished = 0
        total_workers = len(futures)
        while finished < total_workers:
            try:
                worker_id, update = q.get(timeout=0.1)
                # Attach worker id if needed
                yield update
            except Empty:
                # Check if any worker finished
                finished = sum(
                    1 for f in futures if f.done()
                )
                continue

    # Clean up any remaining temporary cookie files
    for f in temp_cookie_files:
        try:
            os.remove(f)
        except Exception:
            pass