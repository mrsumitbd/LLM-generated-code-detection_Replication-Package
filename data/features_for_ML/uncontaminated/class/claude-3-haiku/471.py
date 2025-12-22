class ChunkDiff:
    """Represents differences between new and existing chunks for smart updates."""

    def __init__(self, new_chunk, existing_chunk):
        self.new_chunk = new_chunk
        self.existing_chunk = existing_chunk
        self.added_lines = []
        self.removed_lines = []
        self.modified_lines = []
        self.compute_diff()

    def compute_diff(self):
        new_lines = self.new_chunk.splitlines()
        existing_lines = self.existing_chunk.splitlines()

        for i, line in enumerate(new_lines):
            if i >= len(existing_lines) or line != existing_lines[i]:
                self.added_lines.append(line)

        for i, line in enumerate(existing_lines):
            if i >= len(new_lines) or line != new_lines[i]:
                self.removed_lines.append(line)

        for i, line in enumerate(new_lines):
            if i < len(existing_lines) and line != existing_lines[i]:
                self.modified_lines.append((existing_lines[i], line))

    def has_changes(self):
        return bool(self.added_lines or self.removed_lines or self.modified_lines)

    def get_changes(self):
        return {
            "added": self.added_lines,
            "removed": self.removed_lines,
            "modified": self.modified_lines,
        }