class CommandsCfg:
    """Command terms for the MDP."""

    def __init__(self):
        self.move_up = "up"
        self.move_down = "down"
        self.move_left = "left"
        self.move_right = "right"
        self.stay = "stay"
        self.pick_up = "pick_up"
        self.drop = "drop"

    def get_move_commands(self):
        return [self.move_up, self.move_down, self.move_left, self.move_right, self.stay]

    def get_all_commands(self):
        return [self.move_up, self.move_down, self.move_left, self.move_right, self.stay, self.pick_up, self.drop]