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
    if response is None:
        return None, FatalException(
            error_code="null_response",
            message="Received null response from OpenAI compatible provider",
            model_provider=model_provider,
            model_name=model_name,
        )
    
    try:
        if not hasattr(response, 'choices') or not response.choices:
            return None, FatalException(
                error_code="no_choices",
                message="Response contains no choices",
                model_provider=model_provider,
                model_name=model_name,
            )
        
        first_choice = response.choices[0]
        
        if isinstance(response, ParsedChatCompletion):
            if not isinstance(first_choice, ParsedChoice):
                return None, FatalException(
                    error_code="invalid_choice_type",
                    message="Expected ParsedChoice for ParsedChatCompletion response",
                    model_provider=model_provider,
                    model_name=model_name,
                )
            return first_choice, None
        else:
            if not isinstance(first_choice, Choice):
                return None, FatalException(
                    error_code="invalid_choice_type",
                    message="Expected Choice for ChatCompletion response",
                    model_provider=model_provider,
                    model_name=model_name,
                )
            return first_choice, None
            
    except AttributeError as e:
        return None, FatalException(
            error_code="invalid_response_structure",
            message=f"Response has invalid structure: {str(e)}",
            model_provider=model_provider,
            model_name=model_name,
        )
    except Exception as e:
        return None, FatalException(
            error_code="response_processing_error",
            message=f"Error processing response: {str(e)}",
            model_provider=model_provider,
            model_name=model_name,
        )