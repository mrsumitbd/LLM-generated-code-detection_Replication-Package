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
	try:
		position = connection.positions_get(ticket=int(id))
		
		if not position:
			return {
				"error": True,
				"message": f"Position with ID {id} not found",
				"data": None
			}
		
		position = position[0]
		
		current_stop_loss = position.sl if stop_loss is None else stop_loss
		current_take_profit = position.tp if take_profit is None else take_profit
		
		request = {
			"action": connection.TRADE_ACTION_SLTP,
			"symbol": position.symbol,
			"sl": current_stop_loss,
			"tp": current_take_profit,
			"position": int(id)
		}
		
		result = connection.order_send(request)
		
		if result.retcode != connection.TRADE_RETCODE_DONE:
			return {
				"error": True,
				"message": f"Failed to modify position: {result.comment}",
				"data": None
			}
		
		updated_position = connection.positions_get(ticket=int(id))
		
		if updated_position:
			return {
				"error": False,
				"message": "Position modified successfully",
				"data": updated_position[0]
			}
		else:
			return {
				"error": True,
				"message": "Position modified but could not retrieve updated data",
				"data": None
			}
	
	except (ValueError, TypeError):
		return {
			"error": True,
			"message": f"Invalid position ID: {id}",
			"data": None
		}
	except Exception as e:
		return {
			"error": True,
			"message": f"Error modifying position: {str(e)}",
			"data": None
		}