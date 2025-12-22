from typing import Any, Dict, Optional, Union
from starlette.responses import JSONResponse

def conflict(
        error: str,
        details: Optional[Union[str, Dict[str, Any]]] = None,
        code: Optional[str] = None,
    ) -> JSONResponse:
        """409 Conflict"""
        return ErrorResponse.create(409, error, details, code)