def get_continuous_action(d_acts, c_act_max, c_act_min, n_bins):
    c_act_max = c_act_max.to(d_acts.device)
    c_act_min = c_act_min.to(d_acts.device)
    c_acts = d_acts / (n_bins - 1) * (c_act_max - c_act_min) + c_act_min
    return c_acts