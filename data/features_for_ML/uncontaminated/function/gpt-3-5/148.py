def get_continuous_action(d_acts, c_act_max, c_act_min, n_bins):
    c_act_range = c_act_max - c_act_min
    bin_width = c_act_range / n_bins
    action_bins = [c_act_min + i * bin_width for i in range(n_bins)]
    
    closest_bin = min(action_bins, key=lambda x: abs(x - d_acts))
    
    return closest_bin