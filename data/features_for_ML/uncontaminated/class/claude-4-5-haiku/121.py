class LLMResponse:
    """
    Base class for LLM response handling with standardized interface for LangGraph.

    Just defines standard getter methods for the ToolCalls, ToolResults, and TextContent.
    """

    def __init__(self, content: Union[str, List[Dict[str, Any]]], status_code: int = 200, raw_logging: bool = False):
        self.content = content
        self.status_code = status_code
        self.raw_logging = raw_logging
        self.tool_calls: List[ToolCall] = []
        self.tool_results: Dict[str, ToolResult] = {}
        self.text_content: str = ""
        self._process_content()
        if self.raw_logging:
            self._log_parsed_response()

    def _process_content(self):
        if isinstance(self.content, str):
            self.text_content = self.content
        elif isinstance(self.content, list):
            for item in self.content:
                if isinstance(item, dict):
                    if "type" in item:
                        if item["type"] == "text":
                            self.text_content += item.get("text", "")
                        elif item["type"] == "tool_use":
                            tool_call = ToolCall(
                                id=item.get("id", ""),
                                name=item.get("name", ""),
                                args=item.get("input", {})
                            )
                            self.tool_calls.append(tool_call)
                        elif item["type"] == "tool_result":
                            tool_result = ToolResult(
                                id=item.get("id", ""),
                                result=item.get("content", "")
                            )
                            self.tool_results[tool_result.id] = tool_result

    def _log_parsed_response(self):
        import logging
        logger = logging.getLogger(__name__)
        logger.debug(f"Parsed LLM Response - Status: {self.status_code}")
        logger.debug(f"Text Content: {self.text_content}")
        logger.debug(f"Tool Calls: {len(self.tool_calls)}")
        logger.debug(f"Tool Results: {len(self.tool_results)}")

    def get_tool_calls(self) -> List[ToolCall]:
        return self.tool_calls

    def get_tool_results(self) -> Dict[str, ToolResult]:
        return self.tool_results

    def get_text_content(self) -> str:
        return self.text_content

    def get_response_data(self) -> LLMResponseData:
        return LLMResponseData(
            tool_calls=self.tool_calls,
            tool_results=self.tool_results,
            text_content=self.text_content,
            status_code=self.status_code
        )