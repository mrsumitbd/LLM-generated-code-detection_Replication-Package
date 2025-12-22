from typing import Optional, Union, Dict, Any
from fastapi.responses import JSONResponse

def conflict(
    error: str,
    details: Optional[Union[str, Dict[str, Any]]] = None,
    code: Optional[str] = None,
) -> JSONResponse:
    """409 Conflict"""
    response = {
        "error": error,
        "details": details,
        "code": code
    }
    return JSONResponse(status_code=409, content=response)