import yt_dlp

def get_soundcloud_track_id(url):
        if "soundcloud.com" in url:
            try:
                ydl_opts = {
                    "quiet": True,
                    "no_warnings": True,
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    return info.get("id")
            except Exception:
                return None
        return None