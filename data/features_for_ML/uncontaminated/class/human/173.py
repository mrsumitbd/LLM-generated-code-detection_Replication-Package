from dataclasses import dataclass, field

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

  id: str
  name: str
  gcs_uri: str
  signed_uri: str
  gcs_fuse_path: str
  mime_type: str
  duration: float
  frames_uris: list[str] | None = field(default_factory=list)