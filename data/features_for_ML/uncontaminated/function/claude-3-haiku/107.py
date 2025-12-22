def find_and_replace_pattern_with_aow_and_update_counters():
    import re

    # Define the pattern to search for
    pattern = r'\b\w+\b'

    # Define the replacement string
    replacement = 'aow'

    # Initialize counters
    total_words = 0
    replaced_words = 0

    # Read the input from the user
    input_text = input("Enter the text to process: ")

    # Find and replace the pattern in the input text
    processed_text = re.sub(pattern, replacement, input_text)

    # Update the counters
    total_words = len(re.findall(pattern, input_text))
    replaced_words = len(re.findall(replacement, processed_text))

    # Print the results
    print("Original text:", input_text)
    print("Processed text:", processed_text)
    print("Total words:", total_words)
    print("Replaced words:", replaced_words)