from datetime import datetime, timedelta

def check_eligibility(last_donation_date_str: str) -> bool:
    """
    Checks if a donor is eligible to donate based on the 90-day rule.

    Args:
        last_donation_date_str (str): The date of the last donation in "YYYY-MM-DD" format.

    Returns:
        bool: True if eligible (90 days or more have passed), False otherwise.
    """
    try:
        last_donation_date = datetime.strptime(last_donation_date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Date string must be in 'YYYY-MM-DD' format")

    today = datetime.now().date()
    days_passed = (today - last_donation_date).days
    
    return days_passed >= 90
