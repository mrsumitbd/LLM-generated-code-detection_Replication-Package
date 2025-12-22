from functools import cached_property
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .volumes import VolumesResource
    from .actions import ActionsResourceWithRawResponse
    from .snapshots import SnapshotsResourceWithRawResponse


class VolumesResourceWithRawResponse:
    """Wraps a :class:`VolumesResource` to expose raw‑response endpoints."""

    def __init__(self, volumes: "VolumesResource") -> None:
        self._volumes = volumes

    @cached_property
    def actions(self) -> "ActionsResourceWithRawResponse":
        """Return the actions sub‑resource with raw‑response support."""
        return ActionsResourceWithRawResponse(self._volumes.actions)

    @cached_property
    def snapshots(self) -> "SnapshotsResourceWithRawResponse":
        """Return the snapshots sub‑resource with raw‑response support."""
        return SnapshotsResourceWithRawResponse(self._volumes.snapshots)