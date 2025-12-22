import anthropic


def stripe_get_customers(api_key: str, **kwargs):
    """
    Get customers from Stripe using Claude as an AI backbone with tool use.
    
    Args:
        api_key: Stripe API key
        **kwargs: Additional arguments to pass to the Stripe API (e.g., limit, starting_after)
    
    Returns:
        List of customers from Stripe
    """
    client = anthropic.Anthropic()
    
    tools = [
        {
            "name": "get_stripe_customers",
            "description": "Retrieve a list of customers from Stripe",
            "input_schema": {
                "type": "object",
                "properties": {
                    "api_key": {
                        "type": "string",
                        "description": "The Stripe API key for authentication"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10."
                    },
                    "starting_after": {
                        "type": "string",
                        "description": "A cursor for use in pagination. starting_after is an object ID that defines your place in the list."
                    }
                },
                "required": ["api_key"]
            }
        }
    ]
    
    tool_input = {"api_key": api_key}
    tool_input.update(kwargs)
    
    messages = [
        {
            "role": "user",
            "content": f"Please retrieve the list of customers from Stripe with the following parameters: {tool_input}"
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
                tool_input_data = content_block.input
                
                if tool_name == "get_stripe_customers":
                    import stripe
                    stripe.api_key = tool_input_data["api_key"]
                    
                    params = {}
                    if "limit" in tool_input_data:
                        params["limit"] = tool_input_data["limit"]
                    if "starting_after" in tool_input_data:
                        params["starting_after"] = tool_input_data["starting_after"]
                    
                    customers = stripe.Customer.list(**params)
                    return customers.data
    
    return []