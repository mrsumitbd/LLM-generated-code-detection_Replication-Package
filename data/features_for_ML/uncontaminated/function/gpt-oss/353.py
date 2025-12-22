from typing import Any, Dict, Optional, Union

from fastapi.responses import JSONResponse


def conflict(
    error: str,
    details: Optional[Union[str, Dict[str, Any]]] = None,
    code: Optional[str] = None,
) -> JSONResponse:
    """409 Conflict"""
    payload: Dict[str, Any] = {"error": error}
    if details is not None:
        payload["details"] = details
    if code is not None:
        payload["code"] = code
    return JSONResponse(status_code=409, content=payload)