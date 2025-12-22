def get_soundcloud_track_id(url):
    track_id = url.split('/')[-1]
    return track_id