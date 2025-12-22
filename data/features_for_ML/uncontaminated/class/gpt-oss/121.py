from typing import Any, Dict, List, Union

# Placeholder imports – replace with actual implementations in your project
try:
    from your_project.types import ToolCall, ToolResult, LLMResponseData
except Exception:
    # Minimal stubs for demonstration purposes
    class ToolCall:
        def __init__(self, name: str, arguments: Any):
            self.name = name
            self.arguments = arguments

        def __repr__(self):
            return f"ToolCall(name={self.name!r}, arguments={self.arguments!r})"

    class ToolResult:
        def __init__(self, name: str, result: Any):
            self.name = name
            self.result = result

        def __repr__(self):
            return f"ToolResult(name={self.name!r}, result={self.result!r})"

    class LLMResponseData:
        def __init__(self, status_code: int, tool_calls: List[ToolCall],
                     tool_results: Dict[str, ToolResult], text_content: str):
            self.status_code = status_code
            self.tool_calls = tool_calls
            self.tool_results = tool_results
            self.text_content = text_content

        def __repr__(self):
            return (f"LLMResponseData(status_code={self.status_code!r}, "
                    f"tool_calls={self.tool_calls!r}, "
                    f"tool_results={self.tool_results!r}, "
                    f"text_content={self.text_content!r})")


class LLMResponse:
    """
    Base class for LLM response handling with standardized interface for LangGraph.

    Just defines standard getter methods for the ToolCalls, ToolResults, and TextContent.
    """

    def __init__(self, content: Union[str, List[Dict[str, Any]]], status_code: int = 200,
                 raw_logging: bool = False):
        self._raw_content = content
        self.status_code = status_code
        self.raw_logging = raw_logging

        # Parsed fields
        self._tool_calls: List[ToolCall] = []
        self._tool_results: Dict[str, ToolResult] = {}
        self._text_content: str = ""

        self._process_content()
        if self.raw_logging:
            self._log_parsed_response()

    def _process_content(self):
        """
        Parse the raw content into tool calls, tool results, and text content.
        """
        if isinstance(self._raw_content, str):
            self._text_content = self._raw_content
            return

        if not isinstance(self._raw_content, list):
            # Unsupported format – treat as empty
            return

        for item in self._raw_content:
            if not isinstance(item, dict):
                continue

            # Text content
            if "content" in item and isinstance(item["content"], str):
                self._text_content += item["content"] + "\n"

            # Tool call
            if "name" in item and "arguments" in item:
                name = item["name"]
                arguments = item["arguments"]
                self._tool_calls.append(ToolCall(name, arguments))

            # Tool result
            if "name" in item and "result" in item:
                name = item["name"]
                result = item["result"]
                self._tool_results[name] = ToolResult(name, result)

        # Strip trailing newline from text content
        self._text_content = self._text_content.strip()

    def _log_parsed_response(self):
        """
        Log the parsed response for debugging purposes.
        """
        print("=== Parsed LLM Response ===")
        print(f"Status Code: {self.status_code}")
        print(f"Text Content:\n{self._text_content}")
        print(f"Tool Calls: {self._tool_calls}")
        print(f"Tool Results: {self._tool_results}")
        print("============================")

    def get_tool_calls(self) -> List[ToolCall]:
        """
        Return the list of parsed tool calls.
        """
        return self._tool_calls

    def get_tool_results(self) -> Dict[str, ToolResult]:
        """
        Return a dictionary mapping tool names to their results.
        """
        return self._tool_results

    def get_text_content(self) -> str:
        """
        Return the concatenated text content of the response.
        """
        return self._text_content

    def get_response_data(self) -> LLMResponseData:
        """
        Return a structured LLMResponseData object containing all parsed data.
        """
        return LLMResponseData(
            status_code=self.status_code,
            tool_calls=self._tool_calls,
            tool_results=self._tool_results,
            text_content=self._text_content,
        )