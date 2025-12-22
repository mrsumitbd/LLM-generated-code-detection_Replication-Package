import numpy as np
from .utils import state_to_sentences, convert_frozenlake_state_to_relative_list

def get_env_state(self):
        """
        Get the current state of the environment as a dictionary.
        
        Returns:
            Dict: Contains player position, target position, and hole positions
                as coordinate tuples (row, col)
        """
        # Get dimensions of the grid
        nrow, ncol = self.gym_env.desc.shape
        

        player_position = player_position = tuple(map(int, self._get_player_position()))
        
        target_position = tuple(map(int, np.argwhere(self.gym_env.desc == b'G')[0]))
        
        hole_positions = [tuple(map(int, pos)) for pos in np.argwhere(self.gym_env.desc == b'H')]
        state_dict={
            "player_position": player_position,
            "target_position": target_position,
            "hole_positions": hole_positions,
            "grid_size": (nrow, ncol),
        }
        return convert_frozenlake_state_to_relative_list(state_dict)