from datetime import datetime


def get_user_age(birth_date):
    format_string = "%Y-%m-%d"
    parsed_time = datetime.strptime(birth_date, format_string)
    today = datetime.today()
    age = (
        today.year
        - parsed_time.year
        - ((today.month, today.day) < (parsed_time.month, parsed_time.day))
    )
    return age
