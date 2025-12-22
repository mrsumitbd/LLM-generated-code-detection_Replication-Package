def Topeol_opt_init(tp, tf):
    import numpy as np
    from scipy.optimize import minimize

    def objective_function(x):
        return np.sum(np.abs(x))

    def constraint_function(x):
        return np.sum(x) - 1

    x0 = np.ones(tp) / tp
    bounds = [(0, 1)] * tp
    constraints = {'type': 'eq', 'fun': constraint_function}

    res = minimize(objective_function, x0, method='SLSQP', bounds=bounds, constraints=constraints)

    return res.x