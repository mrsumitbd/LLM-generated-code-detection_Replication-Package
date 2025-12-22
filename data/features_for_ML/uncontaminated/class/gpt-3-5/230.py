from typing import Optional, Set, Tuple, List, Dict, Any

class LLMRequest:
    """LLM请求类"""

    def __init__(self, model_set: TaskConfig, request_type: str = "") -> None:
        self.model_set = model_set
        self.request_type = request_type

    def _select_model(self, exclude_models: Optional[Set[str]] = None) -> Tuple[ModelInfo, APIProvider, BaseClient]:
        # Implementation goes here
        pass

    def _build_tool_options(self, tools: Optional[List[Dict[str, Any]]]) -> Optional[List[ToolOption]]:
        # Implementation goes here
        pass

    @staticmethod
    def _extract_reasoning(content: str) -> Tuple[str, str]:
        # Implementation goes here
        pass