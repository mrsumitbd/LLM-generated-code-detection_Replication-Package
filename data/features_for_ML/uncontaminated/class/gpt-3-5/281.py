class CommandsCfg:
    """Command terms for the MDP."""
    
    def __init__(self, move_forward, move_backward, turn_left, turn_right, stay_still):
        self.move_forward = move_forward
        self.move_backward = move_backward
        self.turn_left = turn_left
        self.turn_right = turn_right
        self.stay_still = stay_still

    def get_move_forward(self):
        return self.move_forward

    def get_move_backward(self):
        return self.move_backward

    def get_turn_left(self):
        return self.turn_left

    def get_turn_right(self):
        return self.turn_right

    def get_stay_still(self):
        return self.stay_still

# Example usage:
# commands = CommandsCfg("forward", "backward", "left", "right", "stay")
# print(commands.get_move_forward())  # Output: forward