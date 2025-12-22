from typing import Union, List, Dict, Any

class LLMResponse:
    """
    Base class for LLM response handling with standardized interface for LangGraph.

    Just defines standard getter methods for the ToolCalls, ToolResults, and TextContent.
    """

    def __init__(self, content: Union[str, List[Dict[str, Any]]], status_code: int = 200, raw_logging: bool = False):
        self.content = content
        self.status_code = status_code
        self.raw_logging = raw_logging
        self.tool_calls = []
        self.tool_results = {}
        self.text_content = ""
        self.response_data = None
        self._process_content()
        self._log_parsed_response()

    def _process_content(self):
        pass

    def _log_parsed_response(self):
        pass

    def get_tool_calls(self) -> List[ToolCall]:
        return self.tool_calls

    def get_tool_results(self) -> Dict[str, ToolResult]:
        return self.tool_results

    def get_text_content(self) -> str:
        return self.text_content

    def get_response_data(self) -> LLMResponseData:
        return self.response_data