from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
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

    name: str
    gcs_uri: str
    signed_uri: str
    gcs_fuse_path: str
    mime_type: str
    frames_uris: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("`name` must not be empty")
        if not self.gcs_uri.startswith("gs://"):
            raise ValueError("`gcs_uri` must start with 'gs://'")
        if not self.signed_uri.startswith(("http://", "https://")):
            raise ValueError("`signed_uri` must be a valid HTTP/HTTPS URL")
        if not self.mime_type.startswith("video/"):
            raise ValueError("`mime_type` must start with 'video/'")
        if not isinstance(self.frames_uris, list):
            raise TypeError("`frames_uris` must be a list")

    def to_dict(self) -> dict:
        """Return a dictionary representation of the video."""
        return {
            "name": self.name,
            "gcs_uri": self.gcs_uri,
            "signed_uri": self.signed_uri,
            "gcs_fuse_path": self.gcs_fuse_path,
            "mime_type": self.mime_type,
            "frames_uris": list(self.frames_uris),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Video":
        """Create a Video instance from a dictionary."""
        return cls(
            name=data["name"],
            gcs_uri=data["gcs_uri"],
            signed_uri=data["signed_uri"],
            gcs_fuse_path=data["gcs_fuse_path"],
            mime_type=data["mime_type"],
            frames_uris=data.get("frames_uris", []),
        )