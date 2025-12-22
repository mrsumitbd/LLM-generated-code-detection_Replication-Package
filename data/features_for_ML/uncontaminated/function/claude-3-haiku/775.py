def preprocess_profile(profile):
    # Check if the input profile is a dictionary
    if not isinstance(profile, dict):
        return None

    # Extract the necessary fields from the profile
    name = profile.get('name', '')
    email = profile.get('email', '')
    phone = profile.get('phone', '')
    address = profile.get('address', '')

    # Normalize the fields
    name = name.strip().title()
    email = email.lower().strip()
    phone = ''.join(char for char in phone if char.isdigit())
    address = address.strip().title()

    # Create the preprocessed profile
    preprocessed_profile = {
        'name': name,
        'email': email,
        'phone': phone,
        'address': address
    }

    return preprocessed_profile