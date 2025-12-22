from typing import List, Optional, Dict, Any, Union
import pathlib
import datetime
import json

class LLMResponse:
    """
    Base class for LLM response handling with standardized interface for LangGraph.

    Just defines standard getter methods for the ToolCalls, ToolResults, and TextContent.
    """

    def __init__(self, content: Union[str, List[Dict[str, Any]]], status_code: int = 200, raw_logging: bool = False):
        """
        Initialize an LLM response. The getter methods are used by LangGraphUtils to parse the response.

        Args:
            content: Raw content from the LLM response
            status_code: HTTP status code of the response
            raw_logging: Whether to log parsed response to a file
        """
        self.content = content
        self.text_content = ""
        self.status_code = status_code
        self.tool_calls: List[ToolCall] = []
        self.tool_results: Dict[str, ToolResult] = {} # maps the id of the tool call to the result.
        self.raw_logging = raw_logging

        # Process content to extract tool calls and results
        self._process_content()

        # Log parsed response if enabled
        if self.raw_logging:
            self._log_parsed_response()

    def _process_content(self):
        """
        Base implementation of content processing. Should be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def _log_parsed_response(self):
        """
        Logs the parsed response to a JSON file if raw_logging is enabled.
        """
        if not self.raw_logging:
            return

        # Create logs directory if it doesn't exist
        log_dir = pathlib.Path("logs/llm_logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        # Generate timestamp for the filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        log_file = log_dir / f"{timestamp}_parsed_response.json"

        # Get response data as a dictionary
        response_data = self.get_response_data().dict()

        # Write response data to file
        with open(log_file, "w") as f:
            json.dump(response_data, f, indent=2, default=str)

    def get_tool_calls(self) -> List[ToolCall]:
        """Return list of ToolCall Pydantic models."""
        return self.tool_calls

    def get_tool_results(self) -> Dict[str, ToolResult]:
        """Return dictionary mapping tool call IDs to ToolResult Pydantic models."""
        return self.tool_results

    def get_text_content(self) -> str:
        """Return the text content as a string."""
        return self.text_content

    def get_response_data(self) -> LLMResponseData:
        """Return the complete response data as an LLMResponseData Pydantic model."""
        return LLMResponseData(
            tool_calls=self.get_tool_calls(),
            tool_results=self.get_tool_results(),
            text_content=self.get_text_content()
        )