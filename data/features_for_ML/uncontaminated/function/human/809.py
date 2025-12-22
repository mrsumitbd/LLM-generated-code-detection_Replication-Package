import numpy as np

def residual_simple(params, wl, cmy_model, data, dstm, paper_sens, log_exposure, density_curves, model='model_a', biases=(1,2,2)):
    cmy, _, _, min_sim = density_mid_min_model(params, wl, cmy_model, model)
        
    # bias for out of diagonal crosstalk
    paper_cm = compute_densitometer_crosstalk_matrix(paper_sens, cmy)
    out_of_diagonal_crosstalk = paper_cm.flatten()[[1,2,3,5,6,7]]
    # bias for parallel gammas
    dstm_cm = compute_densitometer_crosstalk_matrix(dstm, cmy)
    gammas = slopes_of_concentrations(log_exposure, density_curves, dstm_cm)
    diff_gammas= gammas - np.mean(gammas)
    
    mid_minus_min_sim = np.sum(cmy, axis=1)
    sim = np.concatenate((mid_minus_min_sim, biases[0]*min_sim))
    res = data - sim
    res = np.concatenate((res, biases[1]*out_of_diagonal_crosstalk, biases[2]*diff_gammas)) # add crosstalk matrix to the loss function
    # 20 is an empirical bias to balance the weight of the crosstalk matrix in the loss function
    return res