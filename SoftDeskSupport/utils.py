import datetime


def get_user_age(birth_date):
    today = datetime.datetime.today()
    age = (today.year - birth_date.year
           - ((today.month, today.day) < (birth_date.month, birth_date.day)))
    return age


def define_can_be_shared(age):
    if age >= 15:
        return True
    else:
        return False
