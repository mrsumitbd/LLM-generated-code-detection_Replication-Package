from datetime import datetime, date

def normalize_age_gender(dob, gen, current_date):
    age = (current_date - dob).days // 365
    gender = 'M' if gen.upper() == 'M' else 'F'
    return age, gender