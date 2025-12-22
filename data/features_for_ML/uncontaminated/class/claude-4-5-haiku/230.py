class LLMRequest:
    """LLM请求类"""

    def __init__(self, model_set: TaskConfig, request_type: str = "") -> None:
        self.model_set = model_set
        self.request_type = request_type
        self.model_info = None
        self.api_provider = None
        self.client = None

    def _select_model(self, exclude_models: Optional[Set[str]] = None) -> Tuple[ModelInfo, APIProvider, BaseClient]:
        if exclude_models is None:
            exclude_models = set()
        
        available_models = [
            model for model in self.model_set.models 
            if model.name not in exclude_models
        ]
        
        if not available_models:
            raise ValueError("No available models found")
        
        selected_model = available_models[0]
        
        api_provider = APIProvider.get_provider(selected_model.provider)
        client = api_provider.get_client(selected_model)
        
        self.model_info = selected_model
        self.api_provider = api_provider
        self.client = client
        
        return selected_model, api_provider, client

    def _build_tool_options(self, tools: Optional[List[Dict[str, Any]]]) -> Optional[List[ToolOption]]:
        if tools is None:
            return None
        
        tool_options = []
        for tool in tools:
            tool_option = ToolOption(
                name=tool.get("name", ""),
                description=tool.get("description", ""),
                parameters=tool.get("parameters", {}),
                required=tool.get("required", [])
            )
            tool_options.append(tool_option)
        
        return tool_options if tool_options else None

    @staticmethod
    def _extract_reasoning(content: str) -> Tuple[str, str]:
        reasoning_start = "<reasoning>"
        reasoning_end = "</reasoning>"
        
        start_idx = content.find(reasoning_start)
        end_idx = content.find(reasoning_end)
        
        if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
            reasoning = content[start_idx + len(reasoning_start):end_idx].strip()
            response = content[:start_idx] + content[end_idx + len(reasoning_end):]
            response = response.strip()
            return reasoning, response
        
        return "", content