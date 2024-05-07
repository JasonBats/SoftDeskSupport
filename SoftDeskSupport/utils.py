import datetime


def get_user_age(birth_date):
    today = datetime.datetime.today()
    birth_date_year = int(birth_date[0:4])
    birth_date_month = int(birth_date[5:7])
    birth_date_day = int(birth_date[8:10])
    age = (today.year - birth_date_year
           - ((today.month, today.day) < (birth_date_month, birth_date_day)))
    return age


def define_can_be_signed_up(age):
    if age >= 15:
        return True
    else:
        return False
