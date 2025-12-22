def handle_url_response(response: ParseResponse) -> FullParseResponse:
    """
    Process a ParseResponse and return a FullParseResponse.
    
    This function takes a ParseResponse object and converts it into a FullParseResponse
    by extracting and organizing the relevant data.
    """
    if not response:
        return FullParseResponse(
            status="error",
            data=None,
            error="Empty response"
        )
    
    try:
        # Extract data from response
        status = getattr(response, 'status', 'unknown')
        data = getattr(response, 'data', None)
        error = getattr(response, 'error', None)
        
        # Process the response
        if status == 'success' and data:
            full_response = FullParseResponse(
                status=status,
                data=data,
                error=None
            )
        elif error:
            full_response = FullParseResponse(
                status='error',
                data=None,
                error=error
            )
        else:
            full_response = FullParseResponse(
                status=status,
                data=data,
                error=error
            )
        
        return full_response
        
    except Exception as e:
        return FullParseResponse(
            status="error",
            data=None,
            error=str(e)
        )