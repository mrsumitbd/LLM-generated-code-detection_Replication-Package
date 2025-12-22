def modify_position(
    connection,
    id: Union[str, int],
    *,
    stop_loss: Optional[Union[int, float]] = None,
    take_profit: Optional[Union[int, float]] = None,
):
    try:
        # Get the current position data
        position_data = connection.get_position(id)

        # Update the stop loss and take profit levels
        if stop_loss is not None:
            position_data['stop_loss'] = stop_loss
        if take_profit is not None:
            position_data['take_profit'] = take_profit

        # Modify the position
        connection.modify_position(position_data)

        # Return the updated position data
        return {'error': False, 'message': 'Position modified successfully', 'data': position_data}
    except Exception as e:
        # Return an error message
        return {'error': True, 'message': str(e)}