from typing import Union, Optional

def modify_position(
    connection,
    id: Union[str, int],
    *,
    stop_loss: Optional[Union[int, float]] = None,
    take_profit: Optional[Union[int, float]] = None,
):
    position_data = connection.get_position_data(id)
    
    if position_data is None:
        return {"error": True, "message": "Position not found", "position_data": None}
    
    if stop_loss is not None:
        position_data['stop_loss'] = stop_loss
    
    if take_profit is not None:
        position_data['take_profit'] = take_profit
    
    connection.update_position_data(id, position_data)
    
    return {"error": False, "message": "Position modified successfully", "position_data": position_data}