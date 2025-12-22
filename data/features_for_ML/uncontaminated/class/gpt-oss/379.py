from typing import Any, Dict, List, Callable


class _Node:
    @staticmethod
    def analyze_knowledge(state: Any) -> Dict[str, Any]:
        """
        Extracts knowledge information from the given state.
        """
        knowledge = getattr(state, "knowledge", None)
        return {"knowledge": knowledge}

    @staticmethod
    def call_tools(state: Any) -> Dict[str, Any]:
        """
        Calls each tool in the state's `tools` attribute if it is callable.
        """
        tools = getattr(state, "tools", [])
        results: Dict[str, Any] = {}
        for tool in tools:
            name = getattr(tool, "name", str(tool))
            try:
                if callable(tool):
                    results[name] = tool()
                else:
                    results[name] = tool
            except Exception as exc:
                results[name] = f"error: {exc}"
        return results

    @staticmethod
    def select_files(state: Any) -> Dict[str, List[str]]:
        """
        Returns the list of files from the state's `files` attribute.
        """
        files = getattr(state, "files", [])
        return {"selected_files": files}