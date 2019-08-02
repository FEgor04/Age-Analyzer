import datetime
import math

import requests

import settings


def get_bdate(target):
    r = requests.get("https://api.vk.com/method/users.get", params={
        "v": settings.version,
        "access_token": settings.token,
        "user_ids": target,
        "fields": "bdate",
        "name_case": "nom"
    })
    return r.json()['response'][0]['bdate']


def get_age(target):
    birth_date_str = get_bdate(target)
    today_date = datetime.datetime.today()
    length = len(birth_date_str)
    if length < 8:
        return "IMPOSSIBLE"
    birth_year = int(birth_date_str[length - 4]) * 1000 + int(birth_date_str[length - 3]) * 100 + int(
        birth_date_str[length - 2]) * 10 + int(birth_date_str[length - 1])
    birth_day = int(birth_date_str[0])
    if birth_date_str[1] != '.':  # В дне рождения два символа.
        birth_day *= 10
        birth_day += int(birth_date_str[1])
        if birth_date_str[4] != '.':  # В месяце рождения два символа
            birth_month = int(birth_date_str[3]) * 10 + int(birth_date_str[4])
        else:
            birth_month = int(birth_date_str[3])
    else:  # В дне рождения один символ
        if birth_date_str[3] != '.':  # В месяце рождения два символа
            birth_month = int(birth_date_str[2]) * 10 + int(birth_date_str[3])
        else:  # В месяце рождения один символ
            birth_month = int(birth_date_str[2])
    birth_date = datetime.date(birth_year, birth_month, birth_day)
    age = today_date.toordinal() - birth_date.toordinal()
    age = age - age / 366
    age = math.floor(age / 365)
    return age


if __name__ == "__main__":
    age = get_age(settings.target)
    print(age)
