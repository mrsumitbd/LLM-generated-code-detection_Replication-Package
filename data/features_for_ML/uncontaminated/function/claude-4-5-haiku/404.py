import anthropic


def choose_language():
    """
    Interactively helps the user choose a programming language using Claude.
    """
    client = anthropic.Anthropic()
    
    print("Welcome to the Programming Language Chooser!")
    print("I'll help you find the best programming language for your needs.\n")
    
    # Gather information about the user's needs
    print("Please answer the following questions:")
    use_case = input("What is your primary use case? (e.g., web development, data science, systems programming, game development): ").strip()
    experience = input("What is your experience level? (beginner, intermediate, advanced): ").strip()
    priorities = input("What are your priorities? (e.g., performance, ease of learning, community support, job market): ").strip()
    constraints = input("Any specific constraints? (e.g., must run on specific platform, need specific libraries): ").strip()
    
    # Create a prompt for Claude
    prompt = f"""Based on the following user profile, recommend the best programming language(s) for them:

Use Case: {use_case}
Experience Level: {experience}
Priorities: {priorities}
Constraints: {constraints}

Please provide:
1. Your top 3 language recommendations
2. For each language, explain why it's suitable for their needs
3. Pros and cons of each recommendation
4. Learning resources or next steps

Be concise but informative."""
    
    # Call Claude API with streaming
    print("\n" + "="*50)
    print("Claude's Recommendation:")
    print("="*50 + "\n")
    
    with client.messages.stream(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
    
    print("\n")


if __name__ == "__main__":
    choose_language()