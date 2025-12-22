import numpy as np

def Topeol_opt_init(tp, tf):
    tpn = tp / max(tp[0], tf[0])
    tfn = tf / max(tp[0], tf[0])

    mask = tfn > 0
    rr = np.mean(tpn[mask] / tfn[mask])
    b0 = rr / (1 + rr)

    tpn = b0 * tp / tp[0]
    tfn = (1 - b0) * tf / tf[0]
    return tpn, tfn, b0