def handle_openai_compatible_response(
    model_provider: ModelProvider,
    model_name: str,
    request: FenicCompletionsRequest,
    response: Optional[Union[ChatCompletion, ParsedChatCompletion]],
    request_key_generator: Callable[[FenicCompletionsRequest], str],
) -> tuple[
        Optional[Union[ParsedChoice, Choice]],
        Optional[Union[FatalException, TransientException]]
    ]:
    
    if isinstance(response, ChatCompletion):
        parsed_response = parse_chat_completion(response)
        return parsed_response, None
    elif isinstance(response, ParsedChatCompletion):
        return response, None
    else:
        return None, TransientException("Invalid response type")