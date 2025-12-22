from datetime import date, datetime

def normalize_age_gender(dob, gen, current_date):
    """
    Normalizes a date of birth and gender string.

    Parameters
    ----------
    dob : str | datetime.date | datetime.datetime
        The date of birth. If a string, it must be in ISO format
        (YYYY-MM-DD) or a format accepted by `datetime.fromisoformat`.
    gen : str
        The gender string. Common values are 'M', 'F', 'Male', 'Female',
        'Male ', ' female', etc. Any unrecognised value is mapped to
        'O' (Other).
    current_date : datetime.date | datetime.datetime
        The reference date used to compute the age. If a datetime
        instance is supplied, its date component is used.

    Returns
    -------
    age : int
        Age in full years as of `current_date`. If `dob` is in the
        future relative to `current_date`, age is returned as 0.
    gender : str
        Normalised gender code: 'M', 'F', or 'O'.

    Raises
    ------
    ValueError
        If `dob` cannot be parsed into a date.
    """
    # ---- Parse dob ----
    if isinstance(dob, (datetime, date)):
        dob_date = dob.date() if isinstance(dob, datetime) else dob
    elif isinstance(dob, str):
        try:
            dob_date = datetime.fromisoformat(dob).date()
        except Exception as exc:
            raise ValueError(f"Unable to parse dob '{dob}': {exc}") from exc
    else:
        raise ValueError(f"Unsupported type for dob: {type(dob)}")

    # ---- Parse current_date ----
    if isinstance(current_date, (datetime, date)):
        cur_date = current_date.date() if isinstance(current_date, datetime) else current_date
    else:
        raise ValueError(f"Unsupported type for current_date: {type(current_date)}")

    # ---- Compute age ----
    if dob_date > cur_date:
        age = 0
    else:
        age = cur_date.year - dob_date.year
        if (cur_date.month, cur_date.day) < (dob_date.month, dob_date.day):
            age -= 1

    # ---- Normalize gender ----
    if not isinstance(gen, str):
        gender = 'O'
    else:
        g = gen.strip().lower()
        if g in {'m', 'male', 'man', 'boy'}:
            gender = 'M'
        elif g in {'f', 'female', 'woman', 'girl'}:
            gender = 'F'
        else:
            gender = 'O'

    return age, gender