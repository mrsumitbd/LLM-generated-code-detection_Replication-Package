import anthropic
import json
from typing import Any


class ToolDefinition:
    """Tool definition with metadata"""

    def __init__(
        self,
        name: str,
        description: str,
        input_schema: dict[str, Any],
    ):
        """Initialize a tool definition.

        Args:
            name: The name of the tool
            description: A description of what the tool does
            input_schema: JSON schema describing the tool's input parameters
        """
        self.name = name
        self.description = description
        self.input_schema = input_schema

    def to_dict(self) -> dict[str, Any]:
        """Convert the tool definition to a dictionary format for Claude API.

        Returns:
            Dictionary representation of the tool definition
        """
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
        }

    @staticmethod
    def create_tool(
        name: str,
        description: str,
        properties: dict[str, Any],
        required: list[str] | None = None,
    ) -> "ToolDefinition":
        """Create a tool definition with a standard JSON schema.

        Args:
            name: The name of the tool
            description: A description of what the tool does
            properties: Dictionary of property names to their schemas
            required: List of required property names

        Returns:
            A new ToolDefinition instance
        """
        input_schema = {
            "type": "object",
            "properties": properties,
        }
        if required:
            input_schema["required"] = required
        return ToolDefinition(name, description, input_schema)


def main():
    """Main function to demonstrate ToolDefinition usage."""
    # Create a simple calculator tool
    calculator_tool = ToolDefinition.create_tool(
        name="calculator",
        description="Performs basic arithmetic operations",
        properties={
            "operation": {
                "type": "string",
                "enum": ["add", "subtract", "multiply", "divide"],
                "description": "The arithmetic operation to perform",
            },
            "a": {
                "type": "number",
                "description": "The first number",
            },
            "b": {
                "type": "number",
                "description": "The second number",
            },
        },
        required=["operation", "a", "b"],
    )

    # Create a weather tool
    weather_tool = ToolDefinition.create_tool(
        name="get_weather",
        description="Gets the current weather for a location",
        properties={
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA",
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Temperature unit",
            },
        },
        required=["location"],
    )

    # Create a custom tool with direct schema
    custom_tool = ToolDefinition(
        name="custom_tool",
        description="A custom tool with specific schema",
        input_schema={
            "type": "object",
            "properties": {
                "param1": {"type": "string"},
                "param2": {"type": "integer"},
            },
            "required": ["param1"],
        },
    )

    # Initialize Anthropic client
    client = anthropic.Anthropic()

    # Create a message with tools
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        tools=[
            calculator_tool.to_dict(),
            weather_tool.to_dict(),
            custom_tool.to_dict(),
        ],
        messages=[
            {
                "role": "user",
                "content": "What is 25 + 17? Also, what's the weather like in New York?",
            }
        ],
    )

    # Process the response
    print("Response from Claude:")
    print(json.dumps(response.model_dump(), indent=2))

    # Check if Claude wants to use tools
    for content_block in response.content:
        if content_block.type == "tool_use":
            print(f"\nTool used: {content_block.name}")
            print(f"Tool input: {json.dumps(content_block.input, indent=2)}")


if __name__ == "__main__":
    main()