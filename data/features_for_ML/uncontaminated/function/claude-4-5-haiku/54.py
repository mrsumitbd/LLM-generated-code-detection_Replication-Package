import anthropic


def generate_lossy_approval_comment(source_url, filenames, force_prompt_lossy_master=False):
    """
    Generate an approval comment for lossy file conversions using Claude.
    
    Args:
        source_url: URL or path to the source file
        filenames: List of output filenames
        force_prompt_lossy_master: Whether to force lossy master prompt
    
    Returns:
        Generated approval comment string
    """
    client = anthropic.Anthropic()
    
    # Format the filenames for the prompt
    filenames_str = "\n".join(f"- {filename}" for filename in filenames)
    
    # Create the prompt
    prompt = f"""You are reviewing a lossy file conversion process. 
    
Source file: {source_url}
Output files:
{filenames_str}

{"This is a lossy master conversion." if force_prompt_lossy_master else ""}

Please generate a brief, professional approval comment for this conversion. The comment should:
1. Acknowledge the conversion has been completed
2. List the output files
3. Note any important considerations about lossy conversion
4. Be suitable for a code review or approval workflow

Keep the comment concise (2-3 sentences)."""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text


if __name__ == "__main__":
    # Example usage
    source = "image.png"
    outputs = ["image_compressed.jpg", "image_thumbnail.jpg"]
    
    comment = generate_lossy_approval_comment(source, outputs)
    print("Generated approval comment:")
    print(comment)