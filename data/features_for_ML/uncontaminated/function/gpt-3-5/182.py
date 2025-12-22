def extract_request_content(message_text):
    start_index = message_text.find('<request>') + len('<request>')
    end_index = message_text.find('</request>')
    return message_text[start_index:end_index] if start_index != -1 and end_index != -1 else ''