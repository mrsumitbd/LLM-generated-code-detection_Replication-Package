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
    try:
        if response is None:
            return None, None

        if isinstance(response, ChatCompletion):
            parsed_response = ParsedChatCompletion.from_chat_completion(response)
        else:
            parsed_response = response

        request_key = request_key_generator(request)
        parsed_choice = parsed_response.get_choice(request_key)

        return parsed_choice, None
    except FatalException as e:
        return None, e
    except TransientException as e:
        return None, e