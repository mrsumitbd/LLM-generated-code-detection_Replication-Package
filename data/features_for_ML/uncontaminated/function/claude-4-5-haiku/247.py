import anthropic


def stream_output(stream, prefix):
    """Stream output from Claude API and print with a prefix."""
    for text in stream.text_stream:
        print(f"{prefix}{text}", end="", flush=True)
    print()  # Add newline at the end


def main():
    client = anthropic.Anthropic()
    
    # Create a streaming message
    with client.messages.stream(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Write a short poem about Python programming."}
        ],
    ) as stream:
        stream_output(stream, ">> ")


if __name__ == "__main__":
    main()