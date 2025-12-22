import json
from pathlib import Path
from typing import Any, Dict, List


class ConversationQualityAnalyzer:
    """Analyze code quality patterns in conversations."""

    def analyze_conversation_file(self, jsonl_path: Path) -> Dict[str, Any]:
        """
        Analyze a single JSONL conversation file.

        The file is expected to contain one JSON object per line with at least
        the following keys:
            - "user": identifier of the speaker
            - "message": the text of the message

        Returns a dictionary with basic quality metrics:
            - total_messages: total number of messages
            - avg_message_length: average number of characters per message
            - unique_users: number of distinct users
            - longest_message: length of the longest message
            - shortest_message: length of the shortest message
        """
        if not jsonl_path.is_file():
            raise FileNotFoundError(f"File not found: {jsonl_path}")

        total_messages = 0
        total_length = 0
        longest = 0
        shortest = None
        users: set[str] = set()

        with jsonl_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue  # skip malformed lines

                message = obj.get("message", "")
                user = obj.get("user", None)

                if user is not None:
                    users.add(user)

                msg_len = len(message)
                total_messages += 1
                total_length += msg_len
                if msg_len > longest:
                    longest = msg_len
                if shortest is None or msg_len < shortest:
                    shortest = msg_len

        avg_length = total_length / total_messages if total_messages else 0

        return {
            "file": str(jsonl_path),
            "total_messages": total_messages,
            "avg_message_length": avg_length,
            "unique_users": len(users),
            "longest_message": longest,
            "shortest_message": shortest or 0,
        }

    def _default_quality(self) -> Dict[str, Any]:
        """
        Return a default quality dictionary with zeroed metrics.
        """
        return {
            "total_messages": 0,
            "avg_message_length": 0.0,
            "unique_users": 0,
            "longest_message": 0,
            "shortest_message": 0,
        }

    def analyze_project(self, project_path: Path, limit: int = 5) -> Dict[str, Any]:
        """
        Analyze all JSONL conversation files in a project directory.

        Parameters
        ----------
        project_path : Path
            Directory containing conversation JSONL files.
        limit : int, optional
            Maximum number of files to analyze. Defaults to 5.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing:
                - "files": list of per-file analysis results
                - "overall": aggregated metrics across all analyzed files
        """
        if not project_path.is_dir():
            raise NotADirectoryError(f"Directory not found: {project_path}")

        jsonl_files: List[Path] = sorted(
            project_path.rglob("*.jsonl")
        )[:limit]

        files_results: List[Dict[str, Any]] = []
        overall = self._default_quality()

        for file_path in jsonl_files:
            result = self.analyze_conversation_file(file_path)
            files_results.append(result)

            # Aggregate metrics
            overall["total_messages"] += result["total_messages"]
            overall["unique_users"] += result["unique_users"]
            overall["longest_message"] = max(
                overall["longest_message"], result["longest_message"]
            )
            overall["shortest_message"] = min(
                overall["shortest_message"] or result["shortest_message"],
                result["shortest_message"],
            )
            overall["avg_message_length"] += result["avg_message_length"]

        # Finalize overall averages
        file_count = len(files_results)
        if file_count:
            overall["avg_message_length"] /= file_count

        return {"files": files_results, "overall": overall}