import anthropic


def chessboard(*args, **kwargs):
    """
    Generate a chessboard pattern using Claude API with tool use.
    
    Args:
        *args: Positional arguments (not used)
        **kwargs: Keyword arguments including:
            - size: Size of the chessboard (default: 8)
            - symbol_black: Symbol for black squares (default: "█")
            - symbol_white: Symbol for white squares (default: " ")
    
    Returns:
        str: A string representation of the chessboard
    """
    size = kwargs.get("size", 8)
    symbol_black = kwargs.get("symbol_black", "█")
    symbol_white = kwargs.get("symbol_white", " ")
    
    client = anthropic.Anthropic()
    
    tools = [
        {
            "name": "generate_chessboard",
            "description": "Generate a chessboard pattern with specified parameters",
            "input_schema": {
                "type": "object",
                "properties": {
                    "size": {
                        "type": "integer",
                        "description": "The size of the chessboard (e.g., 8 for 8x8)"
                    },
                    "black_symbol": {
                        "type": "string",
                        "description": "Symbol to use for black squares"
                    },
                    "white_symbol": {
                        "type": "string",
                        "description": "Symbol to use for white squares"
                    }
                },
                "required": ["size", "black_symbol", "white_symbol"]
            }
        }
    ]
    
    messages = [
        {
            "role": "user",
            "content": f"Generate a {size}x{size} chessboard using the generate_chessboard tool with black_symbol='{symbol_black}' and white_symbol='{symbol_white}'"
        }
    ]
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )
    
    while response.stop_reason == "tool_use":
        tool_use_block = None
        for block in response.content:
            if block.type == "tool_use":
                tool_use_block = block
                break
        
        if tool_use_block is None:
            break
        
        tool_name = tool_use_block.name
        tool_input = tool_use_block.input
        
        if tool_name == "generate_chessboard":
            board_size = tool_input.get("size", 8)
            black_sym = tool_input.get("black_symbol", "█")
            white_sym = tool_input.get("white_symbol", " ")
            
            board = []
            for row in range(board_size):
                row_str = ""
                for col in range(board_size):
                    if (row + col) % 2 == 0:
                        row_str += white_sym
                    else:
                        row_str += black_sym
                board.append(row_str)
            
            chessboard_result = "\n".join(board)
            
            messages.append({"role": "assistant", "content": response.content})
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use_block.id,
                        "content": chessboard_result
                    }
                ]
            })
            
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                tools=tools,
                messages=messages
            )
    
    for block in response.content:
        if hasattr(block, "text"):
            return block.text
    
    board = []
    for row in range(size):
        row_str = ""
        for col in range(size):
            if (row + col) % 2 == 0:
                row_str += symbol_white
            else:
                row_str += symbol_black
        board.append(row_str)
    
    return "\n".join(board)


if __name__ == "__main__":
    result = chessboard(size=8, symbol_black="█", symbol_white=" ")
    print(result)