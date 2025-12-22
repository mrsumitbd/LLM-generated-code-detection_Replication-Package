def calculateAge(timedelta_obj):
    years = timedelta_obj.days // 365
    months = (timedelta_obj.days % 365) // 30
    days = (timedelta_obj.days % 365) % 30
    return years, months, days