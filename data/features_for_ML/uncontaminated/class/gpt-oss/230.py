from __future__ import annotations

from typing import Any, Dict, List, Optional, Set, Tuple

# Placeholder types for external dependencies
class TaskConfig:
    """Placeholder for TaskConfig. Expected to have a `models` attribute."""
    def __init__(self, models: List[Any]):
        self.models = models

class ModelInfo:
    """Placeholder for ModelInfo."""
    pass

class APIProvider:
    """Placeholder for APIProvider."""
    pass

class BaseClient:
    """Placeholder for BaseClient."""
    pass

class ToolOption:
    """Placeholder for ToolOption."""
    def __init__(self, name: str, description: str, function: Any):
        self.name = name
        self.description = description
        self.function = function

class LLMRequest:
    """LLM请求类"""

    def __init__(self, model_set: TaskConfig, request_type: str = "") -> None:
        self.model_set = model_set
        self.request_type = request_type
        self.selected_model: Optional[ModelInfo] = None
        self.provider: Optional[APIProvider] = None
        self.client: Optional[BaseClient] = None

    def _select_model(self, exclude_models: Optional[Set[str]] = None) -> Tuple[ModelInfo, APIProvider, BaseClient]:
        """
        Select a model from the provided TaskConfig, excluding any models in `exclude_models`.
        Returns a tuple of (ModelInfo, APIProvider, BaseClient).
        """
        if exclude_models is None:
            exclude_models = set()

        # Find the first model not in the exclude list
        for model in self.model_set.models:
            # Assume each model has an attribute `name`
            model_name = getattr(model, "name", None)
            if model_name is None or model_name in exclude_models:
                continue
            # Instantiate provider and client (placeholder logic)
            provider = APIProvider()
            client = BaseClient()
            self.selected_model = model
            self.provider = provider
            self.client = client
            return model, provider, client

        # If no suitable model found, raise an error
        raise ValueError("No suitable model found after applying exclusions.")

    def _build_tool_options(self, tools: Optional[List[Dict[str, Any]]]) -> Optional[List[ToolOption]]:
        """
        Convert a list of tool dictionaries into a list of ToolOption objects.
        Each tool dict is expected to contain 'name', 'description', and 'function'.
        """
        if not tools:
            return None

        tool_options: List[ToolOption] = []
        for tool_dict in tools:
            name = tool_dict.get("name", "")
            description = tool_dict.get("description", "")
            function = tool_dict.get("function", None)
            tool_options.append(ToolOption(name=name, description=description, function=function))
        return tool_options

    @staticmethod
    def _extract_reasoning(content: str) -> Tuple[str, str]:
        """
        Extract reasoning and final answer from a content string.
        Looks for markers '## Reasoning:' and '## Final:'.
        If markers are not found, returns the entire content as reasoning and an empty final answer.
        """
        reasoning_marker = "## Reasoning:"
        final_marker = "## Final:"

        reasoning = ""
        final = ""

        # Find indices of markers
        reasoning_start = content.find(reasoning_marker)
        final_start = content.find(final_marker)

        if reasoning_start != -1:
            # Reasoning starts after the marker
            reasoning_start += len(reasoning_marker)
            if final_start != -1:
                reasoning = content[reasoning_start:final_start].strip()
                final = content[final_start + len(final_marker):].strip()
            else:
                reasoning = content[reasoning_start:].strip()
        elif final_start != -1:
            # No reasoning marker, but final marker exists
            final = content[final_start + len(final_marker):].strip()
            reasoning = ""
        else:
            # No markers found
            reasoning = content.strip()
            final = ""

        return reasoning, final