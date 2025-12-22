import anthropic


def validate_expression(expression: str, allowed_keys: list[str]) -> None:
    """
    Validates a mathematical expression using Claude API.
    
    Args:
        expression: A mathematical expression string to validate
        allowed_keys: A list of allowed variable names in the expression
        
    Raises:
        ValueError: If the expression is invalid or contains disallowed variables
    """
    client = anthropic.Anthropic()
    
    prompt = f"""Validate the following mathematical expression and check if it only uses allowed variables.

Expression: {expression}
Allowed variables: {', '.join(allowed_keys) if allowed_keys else 'none (only constants allowed)'}

Please check:
1. Is the expression syntactically valid as a mathematical expression?
2. Does it only use the allowed variables (and mathematical operators/functions)?
3. Are there any security concerns or invalid characters?

Respond with ONLY "VALID" if the expression passes all checks, or "INVALID: [reason]" if it fails."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    response = message.content[0].text.strip()
    
    if response.startswith("INVALID"):
        raise ValueError(response.replace("INVALID: ", ""))
    elif response != "VALID":
        raise ValueError(f"Unexpected validation response: {response}")


if __name__ == "__main__":
    # Test cases
    test_cases = [
        ("x + y", ["x", "y"], True),
        ("x + y", ["x"], False),
        ("2 * 3 + 4", [], True),
        ("x**2 + 2*x + 1", ["x"], True),
        ("import os; os.system('rm -rf /')", ["x"], False),
        ("sin(x) + cos(y)", ["x", "y"], True),
        ("undefined_var + 5", ["x"], False),
    ]
    
    for expr, allowed, should_pass in test_cases:
        try:
            validate_expression(expr, allowed)
            result = "PASSED" if should_pass else "FAILED (should have raised)"
        except ValueError as e:
            result = "FAILED (raised)" if should_pass else "PASSED"
            print(f"  Error: {e}")
        
        print(f"Expression: {expr}")
        print(f"Allowed: {allowed}")
        print(f"Result: {result}\n")