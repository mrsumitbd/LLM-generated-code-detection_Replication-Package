def calculateAge(timedelta_obj):
    seconds = timedelta_obj.total_seconds()
    years = int(seconds // (365.25 * 24 * 60 * 60))
    remaining_seconds = seconds % (365.25 * 24 * 60 * 60)
    days = int(remaining_seconds // (24 * 60 * 60))
    return years, days