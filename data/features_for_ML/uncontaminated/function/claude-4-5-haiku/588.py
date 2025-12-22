import ast
import anthropic


def handle_launch_config(node: ast.Call, context: ParseContext) -> dict:
    """
    Handle launch configuration nodes in AST.
    
    Args:
        node: An ast.Call node representing a launch configuration
        context: ParseContext containing parsing state and configuration
        
    Returns:
        A dictionary containing the parsed launch configuration
    """
    client = anthropic.Anthropic()
    
    # Convert the AST node to source code for analysis
    node_source = ast.unparse(node)
    
    # Use Claude to analyze the launch configuration
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Analyze this Python launch configuration AST node and extract its configuration details.
                
AST Node source code:
{node_source}

Please provide a JSON response with the following structure:
{{
    "type": "launch_config",
    "function_name": "<name of the launch function>",
    "arguments": {{
        "<arg_name>": "<arg_value or type>"
    }},
    "keywords": {{
        "<keyword_name>": "<keyword_value or type>"
    }},
    "description": "<brief description of what this launch config does>"
}}

Extract all arguments and keyword arguments from the call."""
            }
        ]
    )
    
    # Parse the response
    response_text = message.content[0].text
    
    # Extract JSON from the response
    import json
    import re
    
    # Find JSON in the response
    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if json_match:
        try:
            config = json.loads(json_match.group())
        except json.JSONDecodeError:
            # Fallback to basic parsing if JSON extraction fails
            config = {
                "type": "launch_config",
                "function_name": "unknown",
                "arguments": {},
                "keywords": {},
                "description": "Launch configuration"
            }
    else:
        config = {
            "type": "launch_config",
            "function_name": "unknown",
            "arguments": {},
            "keywords": {},
            "description": "Launch configuration"
        }
    
    # Add context information if available
    if hasattr(context, 'file_path'):
        config['file_path'] = context.file_path
    if hasattr(context, 'line_number'):
        config['line_number'] = node.lineno if hasattr(node, 'lineno') else None
    
    return config


class ParseContext:
    """Context for parsing operations."""
    
    def __init__(self, file_path: str = None):
        self.file_path = file_path
        self.line_number = 0