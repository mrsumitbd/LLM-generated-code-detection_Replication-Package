import subprocess
from Crypto.Random import get_random_bytes
from unshackle.core.utilities import get_extension, get_free_port
from pathlib import Path
from typing import Any, Callable, Generator, MutableMapping, Optional, Union
from http.cookiejar import CookieJar
from urllib.parse import urlparse

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
    if proxy and not proxy.lower().startswith("http://"):
        # Only HTTP proxies are supported by aria2(c)
        proxy = urlparse(proxy)

        port = get_free_port()
        username, password = get_random_bytes(8).hex(), get_random_bytes(8).hex()
        local_proxy = f"http://{username}:{password}@localhost:{port}"

        scheme = {"https": "http+ssl", "socks5h": "socks"}.get(proxy.scheme, proxy.scheme)

        remote_server = f"{scheme}://{proxy.hostname}"
        if proxy.port:
            remote_server += f":{proxy.port}"
        if proxy.username or proxy.password:
            remote_server += "#"
        if proxy.username:
            remote_server += proxy.username
        if proxy.password:
            remote_server += f":{proxy.password}"

        p = subprocess.Popen(
            ["pproxy", "-l", f"http://:{port}#{username}:{password}", "-r", remote_server],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        try:
            yield from download(urls, output_dir, filename, headers, cookies, local_proxy, max_workers)
        finally:
            p.kill()
            p.wait()
        return
    yield from download(urls, output_dir, filename, headers, cookies, proxy, max_workers)