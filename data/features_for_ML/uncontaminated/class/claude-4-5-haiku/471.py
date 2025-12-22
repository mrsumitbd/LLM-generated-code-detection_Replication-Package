import anthropic
import json


class ChunkDiff:
    """Represents differences between new and existing chunks for smart updates."""

    def __init__(self, existing_chunk: str, new_chunk: str):
        """Initialize ChunkDiff with existing and new chunks.
        
        Args:
            existing_chunk: The current/existing chunk content
            new_chunk: The new chunk content to compare against
        """
        self.existing_chunk = existing_chunk
        self.new_chunk = new_chunk
        self.client = anthropic.Anthropic()
        self._diff_analysis = None

    def analyze(self) -> dict:
        """Analyze differences between chunks using Claude.
        
        Returns:
            Dictionary containing the analysis of differences
        """
        if self._diff_analysis is not None:
            return self._diff_analysis

        prompt = f"""Analyze the differences between these two text chunks and provide a structured analysis.

Existing chunk:
{self.existing_chunk}

New chunk:
{self.new_chunk}

Provide your analysis in JSON format with the following structure:
{{
    "has_changes": boolean,
    "change_type": "addition" | "deletion" | "modification" | "none",
    "summary": "brief summary of changes",
    "added_content": "content that was added (if any)",
    "removed_content": "content that was removed (if any)",
    "modified_sections": ["list of modified sections"],
    "similarity_score": 0-100
}}

Return only valid JSON, no additional text."""

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        response_text = message.content[0].text
        self._diff_analysis = json.loads(response_text)
        return self._diff_analysis

    def has_changes(self) -> bool:
        """Check if there are any changes between chunks.
        
        Returns:
            True if chunks differ, False otherwise
        """
        analysis = self.analyze()
        return analysis.get("has_changes", False)

    def get_change_type(self) -> str:
        """Get the type of change between chunks.
        
        Returns:
            Type of change: 'addition', 'deletion', 'modification', or 'none'
        """
        analysis = self.analyze()
        return analysis.get("change_type", "none")

    def get_summary(self) -> str:
        """Get a summary of the changes.
        
        Returns:
            Summary string describing the changes
        """
        analysis = self.analyze()
        return analysis.get("summary", "No changes detected")

    def get_added_content(self) -> str:
        """Get content that was added.
        
        Returns:
            String containing added content, or empty string if nothing was added
        """
        analysis = self.analyze()
        return analysis.get("added_content", "")

    def get_removed_content(self) -> str:
        """Get content that was removed.
        
        Returns:
            String containing removed content, or empty string if nothing was removed
        """
        analysis = self.analyze()
        return analysis.get("removed_content", "")

    def get_modified_sections(self) -> list:
        """Get list of modified sections.
        
        Returns:
            List of strings describing modified sections
        """
        analysis = self.analyze()
        return analysis.get("modified_sections", [])

    def get_similarity_score(self) -> int:
        """Get similarity score between chunks.
        
        Returns:
            Similarity score from 0-100
        """
        analysis = self.analyze()
        return analysis.get("similarity_score", 0)

    def should_update(self, threshold: int = 50) -> bool:
        """Determine if chunk should be updated based on similarity threshold.
        
        Args:
            threshold: Similarity threshold below which update is recommended (0-100)
            
        Returns:
            True if update is recommended, False otherwise
        """
        similarity = self.get_similarity_score()
        return similarity < threshold

    def get_full_analysis(self) -> dict:
        """Get the complete analysis of differences.
        
        Returns:
            Dictionary containing all analysis data
        """
        return self.analyze()