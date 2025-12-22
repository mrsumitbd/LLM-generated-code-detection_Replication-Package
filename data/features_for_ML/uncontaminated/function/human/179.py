from app.schemas import MediaInfo, DiscoverMediaSource

def __series_to_media(series_info: dict) -> MediaInfo:
        first_air_date = series_info.get("publishTime")
        poster = series_info.get("h5pics", {}).get("highResolutionV", "")
        if poster:
            poster = poster.replace("http://wapx.cmvideo.cn:8080", "https://wapx.cmvideo.cn")
        return MediaInfo(
            type="电视剧",
            title=series_info.get("name"),
            year=series_info.get("year"),
            title_year=f"{series_info.get('name')} ({series_info.get('year')})",
            mediaid_prefix="migu",
            media_id=str(series_info.get("pID")),
            release_date=series_info.get("publishTime"),
            poster_path=poster,
            vote_average=series_info.get("score"),
            first_air_date=first_air_date,
        )