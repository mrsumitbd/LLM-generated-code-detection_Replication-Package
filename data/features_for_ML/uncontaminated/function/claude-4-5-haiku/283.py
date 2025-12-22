import anthropic
import json
from functools import wraps


def diamond_peptidase_options(func):
    """
    Decorator that adds tool use capabilities to a function using Claude's API.
    The decorated function can call Claude with tool definitions and handle tool calls.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get the tool definitions from the decorated function
        tool_definitions = func(*args, **kwargs)
        
        if not isinstance(tool_definitions, list):
            return tool_definitions
        
        # Initialize the Anthropic client
        client = anthropic.Anthropic()
        
        # Create tools list for Claude
        tools = []
        for tool_def in tool_definitions:
            tools.append({
                "name": tool_def.get("name", ""),
                "description": tool_def.get("description", ""),
                "input_schema": tool_def.get("input_schema", {})
            })
        
        # Create initial message to Claude
        messages = [
            {
                "role": "user",
                "content": "You have access to several tools. Please analyze them and provide information about what they do."
            }
        ]
        
        # Call Claude with tools
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )
        
        # Process the response
        result = {
            "tools": tool_definitions,
            "response": response.content,
            "stop_reason": response.stop_reason
        }
        
        return result
    
    return wrapper


# Example usage and test
@diamond_peptidase_options
def get_peptidase_tools():
    """Define peptidase-related tools for Claude to use."""
    return [
        {
            "name": "analyze_peptide_sequence",
            "description": "Analyzes a peptide sequence for potential cleavage sites",
            "input_schema": {
                "type": "object",
                "properties": {
                    "sequence": {
                        "type": "string",
                        "description": "The peptide sequence to analyze"
                    },
                    "enzyme_type": {
                        "type": "string",
                        "description": "Type of peptidase enzyme"
                    }
                },
                "required": ["sequence", "enzyme_type"]
            }
        },
        {
            "name": "predict_cleavage_sites",
            "description": "Predicts cleavage sites in a protein sequence",
            "input_schema": {
                "type": "object",
                "properties": {
                    "protein_sequence": {
                        "type": "string",
                        "description": "The protein sequence"
                    },
                    "specificity": {
                        "type": "string",
                        "description": "Cleavage specificity (e.g., 'trypsin', 'pepsin')"
                    }
                },
                "required": ["protein_sequence", "specificity"]
            }
        },
        {
            "name": "calculate_fragment_mass",
            "description": "Calculates the mass of peptide fragments",
            "input_schema": {
                "type": "object",
                "properties": {
                    "fragments": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of peptide fragments"
                    }
                },
                "required": ["fragments"]
            }
        }
    ]


if __name__ == "__main__":
    # Test the decorator
    result = get_peptidase_tools()
    
    # Print the results
    print("Tools defined:")
    for tool in result["tools"]:
        print(f"  - {tool['name']}: {tool['description']}")
    
    print("\nClaude's response:")
    print(f"Stop reason: {result['stop_reason']}")
    
    # Print response content
    for content_block in result["response"]:
        if hasattr(content_block, 'text'):
            print(f"Text: {content_block.text}")