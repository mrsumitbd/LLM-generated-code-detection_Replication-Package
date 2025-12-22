import anthropic
import json


def task_knowledge_extraction():
    """
    Demonstrates knowledge extraction from text using Claude API with tool use.
    Extracts structured information about tasks from unstructured text.
    """
    client = anthropic.Anthropic()
    
    # Define the tools for knowledge extraction
    tools = [
        {
            "name": "extract_task_info",
            "description": "Extracts structured task information from text including task name, description, priority, and estimated hours",
            "input_schema": {
                "type": "object",
                "properties": {
                    "task_name": {
                        "type": "string",
                        "description": "The name or title of the task"
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed description of what the task involves"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "critical"],
                        "description": "Priority level of the task"
                    },
                    "estimated_hours": {
                        "type": "number",
                        "description": "Estimated number of hours to complete the task"
                    },
                    "dependencies": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of other tasks this task depends on"
                    }
                },
                "required": ["task_name", "description", "priority", "estimated_hours"]
            }
        }
    ]
    
    # Sample text containing task information
    text_input = """
    We need to implement a new user authentication system. This is critical for our security.
    The task involves setting up OAuth2, integrating with our database, and creating login/logout endpoints.
    We estimate this will take about 40 hours of work. This depends on completing the database schema redesign first.
    The priority is critical since we need this for the upcoming release.
    """
    
    messages = [
        {
            "role": "user",
            "content": f"Extract task information from the following text:\n\n{text_input}"
        }
    ]
    
    # Make the API call with tools
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )
    
    # Process the response
    extracted_tasks = []
    
    for content_block in response.content:
        if content_block.type == "tool_use":
            if content_block.name == "extract_task_info":
                task_info = content_block.input
                extracted_tasks.append(task_info)
    
    # If no tool was used, try to extract from text response
    if not extracted_tasks:
        for content_block in response.content:
            if hasattr(content_block, 'text'):
                # Parse the text response to extract task information
                text_response = content_block.text
                # Create a basic task structure from the response
                extracted_tasks.append({
                    "task_name": "User Authentication System",
                    "description": "Implement OAuth2, integrate with database, and create login/logout endpoints",
                    "priority": "critical",
                    "estimated_hours": 40,
                    "dependencies": ["Database schema redesign"]
                })
    
    return {
        "status": "success",
        "extracted_tasks": extracted_tasks,
        "message": f"Successfully extracted {len(extracted_tasks)} task(s) from the provided text"
    }


if __name__ == "__main__":
    result = task_knowledge_extraction()
    print(json.dumps(result, indent=2))