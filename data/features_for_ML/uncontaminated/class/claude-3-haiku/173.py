class Video:
    """
    Represents a single video asset within a generation response.

    Attributes:
        name: The name of the video file.
        gcs_uri: The Google Cloud Storage (GCS) URI where the video is stored.
        signed_uri: A pre-signed URL for temporary public access to the video.
        gcs_fuse_path: The FUSE path if the GCS bucket is mounted locally.
        mime_type: The MIME type of the video (e.g., 'video/mp4').
        frames_uris: An optional list of GCS URIs for individual frames
                     that comprise the video. Defaults to an empty list.
    """

    def __init__(self, name, gcs_uri, signed_uri, gcs_fuse_path, mime_type, frames_uris=None):
        self.name = name
        self.gcs_uri = gcs_uri
        self.signed_uri = signed_uri
        self.gcs_fuse_path = gcs_fuse_path
        self.mime_type = mime_type
        self.frames_uris = frames_uris or []

    def __str__(self):
        return f"Video(name='{self.name}', gcs_uri='{self.gcs_uri}', signed_uri='{self.signed_uri}', gcs_fuse_path='{self.gcs_fuse_path}', mime_type='{self.mime_type}', frames_uris={self.frames_uris})"

    def __repr__(self):
        return str(self)