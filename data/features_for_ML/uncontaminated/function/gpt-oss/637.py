def Topeol_opt_init(tp, tf):
    import numpy as np
    # Try to interpret tp and tf as dimensions
    try:
        return np.zeros((int(tp), int(tf)))
    except Exception:
        # If they are iterable, use their lengths
        try:
            return np.zeros((len(tp), len(tf)))
        except Exception:
            # Fallback: return the inputs unchanged
            return (tp, tf)