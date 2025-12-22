def create_full_agent(
    model_name: str,
    vision_model_name: str | None,
    no_stream: bool = False,
    compact_every_n_iteration: int | None = None,
    max_tokens_working_memory: int | None = None,
) -> Agent:
    """Create an agent with the specified model and many tools.

    Args:
        model_name (str): Name of the model to use
        vision_model_name (str | None): Name of the vision model to use
        no_stream (bool, optional): If True, the agent will not stream results.
        compact_every_n_iteration (int | None, optional): Frequency of memory compaction.
        max_tokens_working_memory (int | None, optional): Maximum tokens for working memory.

    Returns:
        Agent: An agent with the specified model and tools

    """
    from anthropic import Anthropic
    
    client = Anthropic()
    
    tools = [
        {
            "name": "calculator",
            "description": "Performs mathematical calculations",
            "input_schema": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate"
                    }
                },
                "required": ["expression"]
            }
        },
        {
            "name": "web_search",
            "description": "Searches the web for information",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "file_reader",
            "description": "Reads content from a file",
            "input_schema": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to read"
                    }
                },
                "required": ["file_path"]
            }
        },
        {
            "name": "code_executor",
            "description": "Executes Python code",
            "input_schema": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python code to execute"
                    }
                },
                "required": ["code"]
            }
        }
    ]
    
    agent_config = {
        "model_name": model_name,
        "vision_model_name": vision_model_name,
        "no_stream": no_stream,
        "compact_every_n_iteration": compact_every_n_iteration,
        "max_tokens_working_memory": max_tokens_working_memory,
        "tools": tools,
        "client": client
    }
    
    agent = Agent(**agent_config)
    
    return agent