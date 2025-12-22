import anthropic
import json
from typing import Any, Callable, Optional


class ComputedBindingConfig:
    """Configuration for computed reactive bindings"""

    def __init__(
        self,
        name: str,
        description: str,
        compute_fn: Callable[..., Any],
        dependencies: list[str],
        cache_ttl: Optional[int] = None,
        validate_fn: Optional[Callable[[Any], bool]] = None,
    ):
        """Initialize ComputedBindingConfig.

        Args:
            name: Name of the computed binding
            description: Description of what this binding computes
            compute_fn: Function that computes the value
            dependencies: List of dependency names this binding depends on
            cache_ttl: Time to live for cached values in seconds
            validate_fn: Optional validation function for computed values
        """
        self.name = name
        self.description = description
        self.compute_fn = compute_fn
        self.dependencies = dependencies
        self.cache_ttl = cache_ttl
        self.validate_fn = validate_fn
        self._cache: dict[str, Any] = {}
        self._cache_timestamps: dict[str, float] = {}

    def compute(self, context: dict[str, Any]) -> Any:
        """Compute the binding value using the provided context.

        Args:
            context: Dictionary containing dependency values

        Returns:
            The computed value
        """
        result = self.compute_fn(**context)

        if self.validate_fn and not self.validate_fn(result):
            raise ValueError(f"Validation failed for binding '{self.name}'")

        return result

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to dictionary representation.

        Returns:
            Dictionary representation of the configuration
        """
        return {
            "name": self.name,
            "description": self.description,
            "dependencies": self.dependencies,
            "cache_ttl": self.cache_ttl,
        }

    def get_schema(self) -> dict[str, Any]:
        """Get JSON schema for this binding configuration.

        Returns:
            JSON schema dictionary
        """
        return {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Binding name"},
                "description": {"type": "string", "description": "Binding description"},
                "dependencies": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of dependencies",
                },
                "cache_ttl": {
                    "type": ["integer", "null"],
                    "description": "Cache time to live in seconds",
                },
            },
            "required": ["name", "description", "dependencies"],
        }

    def create_tool_definition(self) -> dict[str, Any]:
        """Create a tool definition for Claude to use this binding.

        Returns:
            Tool definition dictionary
        """
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": {
                    dep: {"type": "string", "description": f"Value for {dep}"}
                    for dep in self.dependencies
                },
                "required": self.dependencies,
            },
        }

    def use_with_claude(
        self, user_message: str, model: str = "claude-3-5-sonnet-20241022"
    ) -> str:
        """Use this binding configuration with Claude API.

        Args:
            user_message: The user's message to send to Claude
            model: The Claude model to use

        Returns:
            Claude's response
        """
        client = anthropic.Anthropic()

        tools = [self.create_tool_definition()]

        messages = [{"role": "user", "content": user_message}]

        response = client.messages.create(
            model=model, max_tokens=1024, tools=tools, messages=messages
        )

        while response.stop_reason == "tool_use":
            tool_use_block = next(
                (block for block in response.content if block.type == "tool_use"),
                None,
            )

            if not tool_use_block:
                break

            tool_name = tool_use_block.name
            tool_input = tool_use_block.input

            if tool_name == self.name:
                try:
                    result = self.compute(tool_input)
                    tool_result = json.dumps(result)
                except Exception as e:
                    tool_result = f"Error: {str(e)}"
            else:
                tool_result = f"Unknown tool: {tool_name}"

            messages.append({"role": "assistant", "content": response.content})
            messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_use_block.id,
                            "content": tool_result,
                        }
                    ],
                }
            )

            response = client.messages.create(
                model=model, max_tokens=1024, tools=tools, messages=messages
            )

        final_response = ""
        for block in response.content:
            if hasattr(block, "text"):
                final_response += block.text

        return final_response