from nat.agent.base import INPUT_SCHEMA_MESSAGE
from langchain_core.tools import BaseTool

def describe_tool(tool: BaseTool) -> str:
            description = f"{tool.name}: {tool.description}"
            if use_tool_schema:
                description += f". {INPUT_SCHEMA_MESSAGE.format(schema=tool.input_schema.model_fields)}"
            return description