def generate_concise_prompt(current_date_time: str, available_tools: dict[str, list[dict[str, Any]]], episodic_memory: list[dict[str, Any]] = None) -> str:
    prompt = f"Current date and time: {current_date_time}\nAvailable tools:\n"
    
    for tool_category, tools in available_tools.items():
        prompt += f"{tool_category}:\n"
        for tool in tools:
            prompt += f"- {tool['name']} ({tool['description']})\n"
    
    if episodic_memory:
        prompt += "Episodic memory:\n"
        for memory in episodic_memory:
            prompt += f"- {memory['event']} ({memory['description']})\n"
    
    return prompt