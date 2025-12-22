def describe_tool(tool: BaseTool) -> str:
    return f"This is a {tool.name} tool with a description of '{tool.description}' and a cost of {tool.cost:.2f} dollars."