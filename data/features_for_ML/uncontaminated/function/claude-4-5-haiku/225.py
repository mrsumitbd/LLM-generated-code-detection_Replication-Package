def calculateAge(timedelta_obj):
    """
    Calculate age in years, months, and days from a timedelta object.
    
    Args:
        timedelta_obj: A timedelta object representing a time duration
        
    Returns:
        A dictionary with keys 'years', 'months', 'days' representing the age
    """
    total_days = timedelta_obj.days
    
    # Calculate years (assuming 365.25 days per year on average)
    years = total_days // 365
    remaining_days = total_days % 365
    
    # Calculate months (assuming 30.44 days per month on average)
    months = remaining_days // 30
    days = remaining_days % 30
    
    return {
        'years': years,
        'months': months,
        'days': days
    }