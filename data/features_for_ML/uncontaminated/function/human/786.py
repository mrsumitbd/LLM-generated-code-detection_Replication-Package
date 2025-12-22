from datetime import datetime

def normalize_age_gender(dob, gen, current_date):
    try:
        birthdate = datetime.strptime(dob, "%Y-%m-%d")
    except Exception:
        birthdate = None

    gender = normalise_gender(gen)
    age = (
        current_date.year
        - birthdate.year
        - ((current_date.month, current_date.day) < (birthdate.month, birthdate.day))
    )
    return age, gender