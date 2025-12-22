def handle_url_response(response: ParseResponse) -> FullParseResponse:
    url = response.url
    status_code = response.status_code
    content = response.content
    headers = response.headers

    if status_code == 200:
        parsed_content = parse_content(content)
        return FullParseResponse(url=url, status_code=status_code, content=parsed_content, headers=headers)
    else:
        return FullParseResponse(url=url, status_code=status_code, content=None, headers=headers)

def parse_content(content: bytes) -> dict:
    # Implement the logic to parse the content and return a dictionary
    parsed_data = {}
    # ...
    return parsed_data