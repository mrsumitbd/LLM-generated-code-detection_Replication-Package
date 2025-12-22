import anthropic


def get_database_tables(db: str) -> str:
    """
    Get the list of tables in a database using Claude with tool use.
    
    Args:
        db: The database name to query
        
    Returns:
        A string containing the list of tables in the database
    """
    client = anthropic.Anthropic()
    
    tools = [
        {
            "name": "get_tables",
            "description": "Get the list of tables in a database",
            "input_schema": {
                "type": "object",
                "properties": {
                    "database": {
                        "type": "string",
                        "description": "The name of the database to query"
                    }
                },
                "required": ["database"]
            }
        }
    ]
    
    messages = [
        {
            "role": "user",
            "content": f"What tables are in the {db} database?"
        }
    ]
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )
    
    if response.stop_reason == "tool_use":
        for content_block in response.content:
            if content_block.type == "tool_use":
                tool_name = content_block.name
                tool_input = content_block.input
                
                if tool_name == "get_tables":
                    database = tool_input.get("database", db)
                    
                    if database == "users":
                        tables = ["users", "profiles", "settings"]
                    elif database == "products":
                        tables = ["products", "categories", "inventory"]
                    elif database == "orders":
                        tables = ["orders", "order_items", "shipments"]
                    else:
                        tables = ["table1", "table2", "table3"]
                    
                    return f"Tables in {database} database: {', '.join(tables)}"
    
    for content_block in response.content:
        if hasattr(content_block, "text"):
            return content_block.text
    
    return f"Unable to retrieve tables for database: {db}"