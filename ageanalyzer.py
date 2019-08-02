# -*- coding: utf-8 -*-

import datetime
import math
from statistics import mean, mode, median

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
    try:
        return r.json()['response'][0]['bdate']
    except:
        return -1;

def get_id_by_domain(target):
    r = requests.get("https://api.vk.com/method/users.get", params={
        "v": settings.version,
        "access_token": settings.token,
        "user_ids": target,
        "fields": "id",
        "name_case": "nom"
    })
    return r.json()['response'][0]['id']

def get_friends(target, count):
    all_data = []
    r = requests.get("https://api.vk.com/method/friends.get", params={
        "v": settings.version,
        "access_token": settings.token,
        "user_id": target,
        "order": "name",
        "count": count,
        "fields": "nickname"
    })
    r = r.json()
    try:
        data = r['response']['items']
    except:
        return -1
    all_data.extend(data)
    if count > 5000:
        r = requests.get("https://api.vk.com/method/friends.get", params={
            "v": settings.version,
            "access_token": settings.token,
            "user_id": target,
            "order": "name",
            "count": count-5000,
            "offset": 5000,
            "fields": "nickname",
            "name_case": "nom"
        })
        data = r.json()
        all_data.extend(data)
    return all_data

def get_average_friends_age(target):
    target_id = get_id_by_domain(target)
    friends = get_friends(target_id, 10000)
    data = []
    if friends == -1:
        return -1
    for i in range(0, friends.__len__()-1):
        age = get_age( friends[i]['id'] )
        if age == -1:
            pass
        else:
            data.append(age)
    return data


def get_age(target):
    birth_date_str = get_bdate(target)
    today_date = datetime.datetime.today()
    if birth_date_str == -1:
        return -1
    length = len(birth_date_str)
    if length < 8:
        return -1
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
    target = settings.target
    age = get_age(target)
    avg_age = get_average_friends_age(target)
    print("Age, judjing by the friends (mean) : {}".format(math.floor(mean(avg_age))))
    print("Age, judjing by the friends (mode) : {}".format(mode(avg_age)))
    print("Age, judjing by the friends (median) : {}".format(math.floor(median(avg_age))))
    print("Age, judjing by the profile: {}".format(age))
