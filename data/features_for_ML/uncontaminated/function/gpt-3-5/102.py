import pickle
import numpy as np

def initialize_from_equilibrium(self):
    with open('initial_guess.pickle', 'rb') as file:
        initial_guess = pickle.load(file)

    # Perform interpolation and mapping to the computational grid
    # Code for interpolation and mapping goes here

    # Example code for interpolation and mapping
    # self.plasma_flux = np.interp(self.eq.grid_points, initial_guess['grid_points'], initial_guess['plasma_flux'])
    # self.corners = initial_guess['corners']