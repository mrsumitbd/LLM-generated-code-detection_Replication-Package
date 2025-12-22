def conflict(
        error: str,
        details: Optional[Union[str, Dict[str, Any]]] = None,
        code: Optional[str] = None,
    ) -> JSONResponse:
    """409 Conflict"""
    body = {"error": error}
    
    if details is not None:
        body["details"] = details
    
    if code is not None:
        body["code"] = code
    
    return JSONResponse(status_code=409, content=body)