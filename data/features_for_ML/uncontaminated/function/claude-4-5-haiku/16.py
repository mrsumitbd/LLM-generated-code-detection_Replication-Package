import anthropic
import json
import re


def search_emails_handler(args, context):
    """
    Handler function that processes email search requests using Claude with tool use.
    
    Args:
        args: Arguments containing the search query
        context: Context information (unused in this implementation)
    
    Returns:
        The final response from Claude after processing the search
    """
    
    # Initialize the Anthropic client
    client = anthropic.Anthropic()
    
    # Define the tools for email operations
    tools = [
        {
            "name": "search_emails",
            "description": "Search for emails based on query criteria like sender, subject, date range, or keywords",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to find emails"
                    },
                    "sender": {
                        "type": "string",
                        "description": "Filter by sender email address"
                    },
                    "subject_keywords": {
                        "type": "string",
                        "description": "Keywords to search in email subjects"
                    },
                    "date_from": {
                        "type": "string",
                        "description": "Start date for email search (YYYY-MM-DD format)"
                    },
                    "date_to": {
                        "type": "string",
                        "description": "End date for email search (YYYY-MM-DD format)"
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "get_email_details",
            "description": "Get detailed information about a specific email",
            "input_schema": {
                "type": "object",
                "properties": {
                    "email_id": {
                        "type": "string",
                        "description": "The ID of the email to retrieve details for"
                    }
                },
                "required": ["email_id"]
            }
        },
        {
            "name": "list_emails",
            "description": "List emails with basic information",
            "input_schema": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of emails to return"
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Number of emails to skip"
                    }
                },
                "required": []
            }
        }
    ]
    
    # Simulated email database
    email_database = [
        {
            "id": "email_001",
            "sender": "john@example.com",
            "subject": "Project Update",
            "date": "2024-01-15",
            "body": "Here's the latest update on the project..."
        },
        {
            "id": "email_002",
            "sender": "sarah@example.com",
            "subject": "Meeting Tomorrow",
            "date": "2024-01-14",
            "body": "Don't forget about our meeting tomorrow at 2 PM..."
        },
        {
            "id": "email_003",
            "sender": "john@example.com",
            "subject": "Budget Review",
            "date": "2024-01-13",
            "body": "Please review the attached budget proposal..."
        },
        {
            "id": "email_004",
            "sender": "admin@example.com",
            "subject": "System Maintenance",
            "date": "2024-01-12",
            "body": "System maintenance scheduled for tonight..."
        },
        {
            "id": "email_005",
            "sender": "sarah@example.com",
            "subject": "Quarterly Report",
            "date": "2024-01-11",
            "body": "The quarterly report is ready for review..."
        }
    ]
    
    def process_tool_call(tool_name, tool_input):
        """Process tool calls and return results"""
        if tool_name == "search_emails":
            query = tool_input.get("query", "").lower()
            sender = tool_input.get("sender", "").lower()
            subject_keywords = tool_input.get("subject_keywords", "").lower()
            date_from = tool_input.get("date_from")
            date_to = tool_input.get("date_to")
            
            results = []
            for email in email_database:
                # Check sender filter
                if sender and sender not in email["sender"].lower():
                    continue
                
                # Check subject keywords
                if subject_keywords and subject_keywords not in email["subject"].lower():
                    continue
                
                # Check date range
                if date_from and email["date"] < date_from:
                    continue
                if date_to and email["date"] > date_to:
                    continue
                
                # Check general query in subject and body
                if query and query not in email["subject"].lower() and query not in email["body"].lower():
                    continue
                
                results.append({
                    "id": email["id"],
                    "sender": email["sender"],
                    "subject": email["subject"],
                    "date": email["date"]
                })
            
            return json.dumps({"results": results, "count": len(results)})
        
        elif tool_name == "get_email_details":
            email_id = tool_input.get("email_id")
            for email in email_database:
                if email["id"] == email_id:
                    return json.dumps(email)
            return json.dumps({"error": f"Email with ID {email_id} not found"})
        
        elif tool_name == "list_emails":
            limit = tool_input.get("limit", 10)
            offset = tool_input.get("offset", 0)
            
            emails = []
            for email in email_database[offset:offset + limit]:
                emails.append({
                    "id": email["id"],
                    "sender": email["sender"],
                    "subject": email["subject"],
                    "date": email["date"]
                })
            
            return json.dumps({"emails": emails, "total": len(email_database)})
        
        return json.dumps({"error": f"Unknown tool: {tool_name}"})
    
    # Prepare the initial message
    user_query = args if isinstance(args, str) else str(args)
    
    messages = [
        {
            "role": "user",
            "content": f"Help me search for emails. Here's what I'm looking for: {user_query}"
        }
    ]
    
    # Agentic loop
    max_iterations = 10
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        
        # Call Claude with tools
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )
        
        # Check if we're done
        if response.stop_reason == "end_turn":
            # Extract the final text response
            for block in response.content:
                if hasattr(block, 'text'):
                    return block.text
            return "Search completed."
        
        # Process tool uses
        if response.stop_reason == "tool_use":
            # Add assistant's response to messages
            messages.append({
                "role": "assistant",
                "content": response.content
            })
            
            # Process each tool use
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_result = process_tool_call(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": tool_result
                    })
            
            # Add tool results to messages
            if tool_results:
                messages.append({
                    "role": "user",
                    "content": tool_results
                })
        else:
            # Unexpected stop reason
            break
    
    return "Search completed after maximum iterations."