import anthropic


def chunk_to_complete_utf8(byte_blocks):
    """
    Takes a list of byte blocks and uses Claude to identify complete UTF-8 sequences.
    Returns a list of complete UTF-8 strings, one for each input block.
    """
    client = anthropic.Anthropic()
    
    results = []
    for block in byte_blocks:
        # Convert bytes to a representation that can be sent to Claude
        hex_repr = block.hex()
        
        # Use Claude to identify complete UTF-8 sequences
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"""Given the following hexadecimal representation of bytes: {hex_repr}

Please identify all complete UTF-8 character sequences in these bytes. A complete UTF-8 sequence is:
- A single byte 0x00-0x7F (ASCII)
- A 2-byte sequence starting with 0xC0-0xDF
- A 3-byte sequence starting with 0xE0-0xEF
- A 4-byte sequence starting with 0xF0-0xF7

Return ONLY the hexadecimal representation of the complete UTF-8 sequences found, with no other text or explanation. If no complete sequences are found, return an empty string."""
                }
            ]
        )
        
        # Extract the response
        response_text = message.content[0].text.strip()
        
        # Convert hex back to bytes and then to string
        if response_text:
            try:
                complete_bytes = bytes.fromhex(response_text)
                complete_str = complete_bytes.decode('utf-8')
                results.append(complete_str)
            except (ValueError, UnicodeDecodeError):
                results.append("")
        else:
            results.append("")
    
    return results


if __name__ == "__main__":
    # Test with some example byte blocks
    test_blocks = [
        b"Hello",  # Complete ASCII
        b"Hel\xc3\xa9",  # "Helé" - complete UTF-8
        b"Test\xc3",  # Incomplete UTF-8 sequence at end
        b"\xe2\x9c\x93",  # Complete UTF-8 for checkmark
        b"\xe2\x9c",  # Incomplete UTF-8
    ]
    
    results = chunk_to_complete_utf8(test_blocks)
    for i, result in enumerate(results):
        print(f"Block {i}: {repr(result)}")