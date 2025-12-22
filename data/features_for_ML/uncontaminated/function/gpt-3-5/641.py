def handle_url_response(response: ParseResponse) -> FullParseResponse:
    full_response = FullParseResponse()
    full_response.status_code = response.status_code
    full_response.headers = response.headers
    full_response.body = response.body
    return full_response