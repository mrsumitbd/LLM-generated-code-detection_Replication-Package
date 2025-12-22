from fastapi import Body, HTTPException, status

def feedback(payload: dict = Body(...)):
    """
    Endpoint to receive user feedback.

    Expected payload keys:
        - name (str)
        - email (str)
        - message (str)

    Returns a JSON response confirming receipt.
    """
    required_keys = {"name", "email", "message"}
    missing = required_keys - payload.keys()
    if missing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required fields: {', '.join(sorted(missing))}",
        )

    # Basic validation: ensure all required fields are non-empty strings
    for key in required_keys:
        value = payload.get(key)
        if not isinstance(value, str) or not value.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Field '{key}' must be a non-empty string.",
            )

    # Here you could add logic to store the feedback, send an email, etc.
    # For now, we simply acknowledge receipt.

    return {
        "status": "success",
        "message": "Feedback received",
        "payload": payload,
    }