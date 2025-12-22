def residual_simple(params, wl, cmy_model, data, dstm, paper_sens, log_exposure, density_curves, model='model_a', biases=(1,2,2)):
    residual = 0
    for i in range(len(data)):
        cmy = cmy_model(params, wl, data[i], dstm, paper_sens, log_exposure, density_curves, model=model, biases=biases)
        residual += (cmy - data[i])**2
    return residual