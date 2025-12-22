def generate_path(duration, mask):
    import numpy as np

    # Convert the mask to a numpy array
    mask_arr = np.array(mask)

    # Calculate the number of steps in the path
    num_steps = np.sum(mask_arr)

    # Initialize the path array
    path = np.zeros((num_steps, 2))

    # Initialize the current position
    current_x = 0
    current_y = 0

    # Initialize the step index
    step_idx = 0

    # Iterate through the mask and generate the path
    for i in range(len(mask_arr)):
        if mask_arr[i] == 1:
            # Update the path
            path[step_idx, 0] = current_x
            path[step_idx, 1] = current_y

            # Update the current position
            if i % 2 == 0:
                current_x += 1
            else:
                current_y += 1

            # Increment the step index
            step_idx += 1

    # Scale the path to the given duration
    path *= (duration / num_steps)

    return path