from fastapi import HTTPException
import os

def sanitize_path(path: str) -> str:
            sanitized_path = os.path.normpath(path.strip("/"))
            if sanitized_path == ".":
                raise HTTPException(status_code=400, detail="Invalid file path.")
            filename = os.path.basename(sanitized_path)
            if not filename:
                raise HTTPException(status_code=400, detail="Filename cannot be empty.")
            return sanitized_path