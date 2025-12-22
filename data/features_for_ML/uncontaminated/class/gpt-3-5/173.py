class Video:
    def __init__(self, name, gcs_uri, signed_uri, gcs_fuse_path, mime_type, frames_uris=None):
        self.name = name
        self.gcs_uri = gcs_uri
        self.signed_uri = signed_uri
        self.gcs_fuse_path = gcs_fuse_path
        self.mime_type = mime_type
        self.frames_uris = frames_uris if frames_uris is not None else []

# Example usage:
video1 = Video("video1.mp4", "gs://bucket/video1.mp4", "https://signedurl.com/video1.mp4", "/mnt/gcs/bucket/video1.mp4", "video/mp4")
print(video1.name)
print(video1.gcs_uri)
print(video1.signed_uri)
print(video1.gcs_fuse_path)
print(video1.mime_type)
print(video1.frames_uris)