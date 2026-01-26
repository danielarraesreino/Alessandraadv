from datetime import timedelta, date

def calculate_business_days(start_date: date, days: int) -> date:
    """
    Calculates the end date after N business days (Monday to Friday).
    According to CPC/2015 and CPP, business days are standard.
    """
    current_date = start_date
    added_days = 0
    while added_days < days:
        current_date += timedelta(days=1)
        if current_date.weekday() < 5:  # 0-4 are Monday to Friday
            added_days += 1
    return current_date
