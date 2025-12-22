import anthropic


def process_statement(statement, column_names=[]):
    """
    Process a SQL statement using Claude to extract information about it.
    
    Args:
        statement: A SQL statement string to process
        column_names: Optional list of column names for context
    
    Returns:
        A dictionary containing the processed information about the statement
    """
    client = anthropic.Anthropic()
    
    # Build the prompt with context about column names if provided
    context = ""
    if column_names:
        context = f"\nAvailable columns: {', '.join(column_names)}"
    
    prompt = f"""Analyze the following SQL statement and provide information about it:

SQL Statement: {statement}{context}

Please provide:
1. The type of statement (SELECT, INSERT, UPDATE, DELETE, etc.)
2. The main tables involved
3. Any WHERE conditions
4. Any JOIN operations
5. Any aggregate functions used
6. A brief description of what this statement does

Format your response as a structured analysis."""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract the response text
    response_text = message.content[0].text
    
    # Parse the response into a structured format
    result = {
        "statement": statement,
        "analysis": response_text,
        "column_names": column_names
    }
    
    return result