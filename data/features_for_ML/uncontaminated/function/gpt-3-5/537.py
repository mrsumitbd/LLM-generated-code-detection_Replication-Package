def get_env_state(self):
    state = {
        'player_position': (self.player_row, self.player_col),
        'target_position': (self.target_row, self.target_col),
        'hole_positions': [(hole_row, hole_col) for hole_row, hole_col in zip(self.hole_rows, self.hole_cols)]
    }
    return state