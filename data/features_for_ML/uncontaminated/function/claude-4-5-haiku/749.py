import anthropic
import json
import re


def audiobookshelf():
    """
    Demonstrates Claude's ability to use tools to interact with an Audiobookshelf API.
    This function sets up tool definitions for common Audiobookshelf operations and
    shows how Claude can use these tools through multi-turn conversations.
    """
    client = anthropic.Anthropic()
    
    # Define the tools that Claude can use to interact with Audiobookshelf
    tools = [
        {
            "name": "get_libraries",
            "description": "Get a list of all libraries in the Audiobookshelf instance",
            "input_schema": {
                "type": "object",
                "properties": {},
                "required": []
            }
        },
        {
            "name": "get_library_items",
            "description": "Get items (books/audiobooks) from a specific library",
            "input_schema": {
                "type": "object",
                "properties": {
                    "library_id": {
                        "type": "string",
                        "description": "The ID of the library to get items from"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of items to return (default: 10)"
                    }
                },
                "required": ["library_id"]
            }
        },
        {
            "name": "search_items",
            "description": "Search for items in Audiobookshelf by title or author",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (title or author name)"
                    },
                    "library_id": {
                        "type": "string",
                        "description": "Optional library ID to search within"
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "get_item_details",
            "description": "Get detailed information about a specific item",
            "input_schema": {
                "type": "object",
                "properties": {
                    "item_id": {
                        "type": "string",
                        "description": "The ID of the item to get details for"
                    }
                },
                "required": ["item_id"]
            }
        },
        {
            "name": "get_user_progress",
            "description": "Get the current listening progress for a user on an item",
            "input_schema": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The ID of the user"
                    },
                    "item_id": {
                        "type": "string",
                        "description": "The ID of the item"
                    }
                },
                "required": ["user_id", "item_id"]
            }
        }
    ]
    
    # Simulated tool responses for demonstration
    def process_tool_call(tool_name, tool_input):
        """Process tool calls and return simulated responses"""
        
        if tool_name == "get_libraries":
            return {
                "libraries": [
                    {"id": "lib1", "name": "Main Library", "mediaType": "book"},
                    {"id": "lib2", "name": "Audiobooks", "mediaType": "audiobook"}
                ]
            }
        
        elif tool_name == "get_library_items":
            library_id = tool_input.get("library_id")
            limit = tool_input.get("limit", 10)
            return {
                "items": [
                    {
                        "id": "item1",
                        "title": "The Great Gatsby",
                        "author": "F. Scott Fitzgerald",
                        "duration": 8.5
                    },
                    {
                        "id": "item2",
                        "title": "To Kill a Mockingbird",
                        "author": "Harper Lee",
                        "duration": 12.3
                    },
                    {
                        "id": "item3",
                        "title": "1984",
                        "author": "George Orwell",
                        "duration": 11.7
                    }
                ][:limit]
            }
        
        elif tool_name == "search_items":
            query = tool_input.get("query", "").lower()
            results = [
                {
                    "id": "item1",
                    "title": "The Great Gatsby",
                    "author": "F. Scott Fitzgerald"
                },
                {
                    "id": "item4",
                    "title": "Gatsby's Ghost",
                    "author": "Unknown"
                }
            ]
            return {
                "results": [r for r in results if query in r["title"].lower() or query in r["author"].lower()]
            }
        
        elif tool_name == "get_item_details":
            item_id = tool_input.get("item_id")
            return {
                "id": item_id,
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "description": "A classic American novel",
                "duration": 8.5,
                "narrator": "Jake Gyllenhaal",
                "releaseDate": "1925"
            }
        
        elif tool_name == "get_user_progress":
            return {
                "userId": tool_input.get("user_id"),
                "itemId": tool_input.get("item_id"),
                "progress": 0.35,
                "currentTime": 3.0,
                "duration": 8.5
            }
        
        return {"error": f"Unknown tool: {tool_name}"}
    
    # Initial user message
    user_message = "I'm looking for audiobooks in my library. Can you help me find 'The Great Gatsby' and tell me about it?"
    
    print(f"User: {user_message}\n")
    
    messages = [
        {"role": "user", "content": user_message}
    ]
    
    # Agentic loop - continue until Claude stops using tools
    while True:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )
        
        # Check if Claude wants to use tools
        if response.stop_reason == "tool_use":
            # Process each tool use in the response
            tool_results = []
            
            for content_block in response.content:
                if content_block.type == "tool_use":
                    tool_name = content_block.name
                    tool_input = content_block.input
                    tool_use_id = content_block.id
                    
                    print(f"Claude is using tool: {tool_name}")
                    print(f"Tool input: {json.dumps(tool_input, indent=2)}")
                    
                    # Get the tool result
                    result = process_tool_call(tool_name, tool_input)
                    print(f"Tool result: {json.dumps(result, indent=2)}\n")
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use_id,
                        "content": json.dumps(result)
                    })
            
            # Add assistant response and tool results to messages
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
            
        else:
            # Claude has finished and provided a final response
            for content_block in response.content:
                if hasattr(content_block, 'text'):
                    print(f"Claude: {content_block.text}")
            break
    
    return "Audiobookshelf interaction completed successfully"


if __name__ == "__main__":
    result = audiobookshelf()
    print(f"\n{result}")