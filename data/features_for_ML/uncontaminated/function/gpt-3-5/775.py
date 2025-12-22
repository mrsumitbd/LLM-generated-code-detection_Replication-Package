def preprocess_profile(profile):
    if 'name' in profile:
        profile['name'] = profile['name'].title()
    if 'age' in profile:
        profile['age'] = int(profile['age'])
    if 'gender' in profile:
        profile['gender'] = profile['gender'].lower()
    return profile