from chunkhound.core.models.chunk import Chunk

class ChunkDiff:
    """Represents differences between new and existing chunks for smart updates."""

    unchanged: list[Chunk]  # Chunks with matching content
    modified: list[Chunk]  # Chunks with different content
    added: list[Chunk]  # New chunks not in existing set
    deleted: list[Chunk]  # Existing chunks not in new set