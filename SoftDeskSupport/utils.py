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


def define_can_be_signed_up(age):
    if age >= 15:
        return True
    else:
        return False
