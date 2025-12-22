from scipy.stats import sem, t, tmean

def _compute_mean_and_conf_int(val):
            if val is None or not isinstance(val, list) or len(val) == 0:
                return (None, None, None)
            mean = tmean(val)
            conf_int = t.interval(
                ci,
                len(val) - 1,
                loc=mean,
                scale=sem(val),
            )
            return (mean, conf_int[0], conf_int[1])