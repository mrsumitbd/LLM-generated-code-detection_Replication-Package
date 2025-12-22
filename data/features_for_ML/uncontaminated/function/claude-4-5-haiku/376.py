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
    import subprocess
    import json
    import re
    from pathlib import Path
    from urllib.parse import urlparse
    from http.cookiejar import CookieJar
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if isinstance(urls, str):
        urls = [urls]
    elif isinstance(urls, dict):
        urls = [urls]
    
    normalized_urls = []
    for i, url_item in enumerate(urls):
        if isinstance(url_item, str):
            normalized_urls.append({"url": url_item, "index": i})
        elif isinstance(url_item, dict):
            normalized_urls.append({**url_item, "index": i})
    
    if max_workers is None:
        from os import cpu_count
        max_workers = min(32, (cpu_count() or 1) + 4)
    
    for url_data in normalized_urls:
        url = url_data["url"]
        index = url_data["index"]
        
        parsed = urlparse(url)
        ext = Path(parsed.path).suffix or ""
        
        output_filename = filename.format(i=index, ext=ext)
        output_path = output_dir / output_filename
        
        cmd = ["aria2c"]
        
        cmd.extend(["--max-concurrent-downloads", str(max_workers)])
        cmd.extend(["-d", str(output_dir)])
        cmd.extend(["-o", output_filename])
        
        if headers:
            for key, value in headers.items():
                if isinstance(value, bytes):
                    value = value.decode("utf-8")
                cmd.extend(["--header", f"{key}: {value}"])
        
        if cookies:
            if isinstance(cookies, CookieJar):
                cookie_str = "; ".join([f"{c.name}={c.value}" for c in cookies])
            else:
                cookie_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])
            cmd.extend(["--header", f"Cookie: {cookie_str}"])
        
        if proxy:
            cmd.extend(["--all-proxy", proxy])
        
        cmd.append(url)
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        
        yield {"total": 100}
        
        last_completed = 0
        last_speed = ""
        
        while True:
            line = process.stdout.readline()
            if not line:
                break
            
            line = line.strip()
            
            match = re.search(r"(\d+)%", line)
            if match:
                completed = int(match.group(1))
                if completed != last_completed:
                    yield {"completed": completed}
                    last_completed = completed
            
            speed_match = re.search(r"([\d.]+\s*[KMG]?B/s)", line)
            if speed_match:
                speed = speed_match.group(1)
                if speed != last_speed:
                    yield {"downloaded": speed}
                    last_speed = speed
        
        process.wait()