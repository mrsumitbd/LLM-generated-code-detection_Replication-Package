from typing import Union, List, Dict, Any
from dataclasses import dataclass

@dataclass
class ToolCall:
    tool_name: str
    tool_input: str

@dataclass
class ToolResult:
    tool_name: str
    tool_output: str

@dataclass
class LLMResponseData:
    tool_calls: List[ToolCall]
    tool_results: Dict[str, ToolResult]
    text_content: str

class LLMResponse:
    """
    Base class for LLM response handling with standardized interface for LangGraph.

    Just defines standard getter methods for the ToolCalls, ToolResults, and TextContent.
    """

    def __init__(self, content: Union[str, List[Dict[str, Any]]], status_code: int = 200, raw_logging: bool = False):
        self.status_code = status_code
        self.raw_logging = raw_logging
        self.content = content
        self._process_content()
        self._log_parsed_response()

    def _process_content(self):
        if isinstance(self.content, str):
            self.response_data = self._parse_text_content(self.content)
        elif isinstance(self.content, list):
            self.response_data = self._parse_structured_content(self.content)
        else:
            raise ValueError("Content must be either a string or a list of dictionaries.")

    def _parse_text_content(self, text_content: str) -> LLMResponseData:
        tool_calls, tool_results = self._extract_tool_calls_and_results(text_content)
        return LLMResponseData(tool_calls, tool_results, text_content)

    def _parse_structured_content(self, structured_content: List[Dict[str, Any]]) -> LLMResponseData:
        tool_calls = []
        tool_results = {}
        text_content = ""

        for item in structured_content:
            if "tool_call" in item:
                tool_call = ToolCall(item["tool_name"], item["tool_input"])
                tool_calls.append(tool_call)
            elif "tool_result" in item:
                tool_result = ToolResult(item["tool_name"], item["tool_output"])
                tool_results[item["tool_name"]] = tool_result
            else:
                text_content += item["text"]

        return LLMResponseData(tool_calls, tool_results, text_content)

    def _extract_tool_calls_and_results(self, text_content: str) -> (List[ToolCall], Dict[str, ToolResult]):
        # Implement logic to extract tool calls and results from the text content
        tool_calls = []
        tool_results = {}
        return tool_calls, tool_results

    def _log_parsed_response(self):
        if self.raw_logging:
            # Implement logic to log the parsed response
            pass

    def get_tool_calls(self) -> List[ToolCall]:
        return self.response_data.tool_calls

    def get_tool_results(self) -> Dict[str, ToolResult]:
        return self.response_data.tool_results

    def get_text_content(self) -> str:
        return self.response_data.text_content

    def get_response_data(self) -> LLMResponseData:
        return self.response_data