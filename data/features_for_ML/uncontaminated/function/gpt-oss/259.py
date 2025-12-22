from typing import Union, Optional

def modify_position(
    connection,
    id: Union[str, int],
    *,
    stop_loss: Optional[Union[int, float]] = None,
    take_profit: Optional[Union[int, float]] = None,
):
    """
    Modify an existing position's stop loss and take profit levels.

    This function attempts to modify the stop loss and take profit of an 
    open position identified by the given ID. If the position ID is invalid 
    or not found, it returns an error. If the modification request is 
    successful, it returns the updated position data.

    Args:
        connection: The connection object to the MetaTrader platform.
        id: The unique identifier of the position to modify.
        stop_loss: The new stop loss level. If None, the current stop loss 
            level is retained.
        take_profit: The new take profit level. If None, the current take 
            profit level is retained.

    Returns:
        A dictionary containing an error flag, a message, and the position 
        data if successful.
    """
    # Basic validation of the id
    if not isinstance(id, (str, int)):
        return {
            "error": True,
            "message": f"Invalid id type: {type(id).__name__}. Expected str or int.",
            "position": None,
        }

    # Validate stop_loss and take_profit if provided
    if stop_loss is not None and not isinstance(stop_loss, (int, float)):
        return {
            "error": True,
            "message": f"stop_loss must be a number or None, got {type(stop_loss).__name__}.",
            "position": None,
        }
    if take_profit is not None and not isinstance(take_profit, (int, float)):
        return {
            "error": True,
            "message": f"take_profit must be a number or None, got {type(take_profit).__name__}.",
            "position": None,
        }

    try:
        # Attempt to modify the position via the connection object.
        # The exact method name may vary; we assume a generic `modify_position`.
        result = connection.modify_position(
            id, stop_loss=stop_loss, take_profit=take_profit
        )

        # If the connection returns a dict with an error flag, propagate it.
        if isinstance(result, dict) and result.get("error"):
            return result

        # Otherwise, construct a success response.
        return {
            "error": False,
            "message": "Position modified successfully.",
            "position": result,
        }

    except Exception as exc:
        # Catch any unexpected errors and return a generic error response.
        return {
            "error": True,
            "message": f"Failed to modify position: {exc}",
            "position": None,
        }