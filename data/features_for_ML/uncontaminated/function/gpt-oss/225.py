def calculateAge(timedelta_obj):
    """
    Calculate the age in whole years from a timedelta object.

    Parameters
    ----------
    timedelta_obj : datetime.timedelta
        The time difference between a birth date and the current date.

    Returns
    -------
    int
        The age in whole years.
    """
    # Use 365.25 days per year to account for leap years
    years = int(timedelta_obj.days / 365.25)
    return years