from datetime import datetime

def normalize_age_gender(dob, gen, current_date):
    dob = datetime.strptime(dob, '%Y-%m-%d')
    age = current_date.year - dob.year - ((current_date.month, current_date.day) < (dob.month, dob.day))
    gender = gen.lower()
    
    return age, gender