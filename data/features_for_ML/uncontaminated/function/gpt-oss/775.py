import re
from datetime import datetime

def preprocess_profile(profile):
    """
    Clean and normalize a profile dictionary.

    - Strip whitespace from keys and string values.
    - Convert numeric strings to int or float.
    - Lower‑case email addresses.
    - Parse common date formats into datetime.date objects.
    - Recursively process nested dictionaries and lists.
    """
    if not isinstance(profile, dict):
        return profile

    cleaned = {}
    for key, value in profile.items():
        # Clean key
        clean_key = key.strip().lower()

        # Process value
        if isinstance(value, str):
            clean_val = value.strip()

            # Email
            if re.match(r"[^@]+@[^@]+\.[^@]+", clean_val):
                clean_val = clean_val.lower()

            # Integer
            elif re.match(r"^\d+$", clean_val):
                clean_val = int(clean_val)

            # Float
            elif re.match(r"^\d+\.\d+$", clean_val):
                clean_val = float(clean_val)

            # Date
            else:
                for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
                    try:
                        clean_val = datetime.strptime(clean_val, fmt).date()
                        break
                    except ValueError:
                        continue

        elif isinstance(value, dict):
            clean_val = preprocess_profile(value)

        elif isinstance(value, list):
            clean_val = [
                preprocess_profile(item) if isinstance(item, dict) else item
                for item in value
            ]

        else:
            clean_val = value

        cleaned[clean_key] = clean_val

    return cleaned