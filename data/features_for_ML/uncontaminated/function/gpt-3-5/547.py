def describe_tool(tool: BaseTool) -> str:
    return f"{tool.name} is a {tool.category} tool used for {tool.purpose}."