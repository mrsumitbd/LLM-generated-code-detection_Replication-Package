def extract_request_content(message_text):
    try:
        start_index = message_text.index('{"') + 1
        end_index = message_text.rindex('}') + 1
        return message_text[start_index:end_index]
    except (ValueError, IndexError):
        return None