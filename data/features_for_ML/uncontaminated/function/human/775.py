def preprocess_profile(profile):
    profile = remove_density_min(profile)
    profile = adjust_log_exposure(profile)
    return profile