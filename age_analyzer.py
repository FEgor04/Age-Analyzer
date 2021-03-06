# -*- coding: utf-8 -*-
import collections
import datetime
import statistics

import requests
from dateutil.relativedelta import relativedelta

import settings


def _counts(data):
    # Generate a table of sorted (value, frequency) pairs.
    table = collections.Counter(iter(data)).most_common()
    if not table:
        return table
    # Extract the values with the highest frequency.
    maxfreq = table[0][1]
    for i in range(1, len(table)):
        if table[i][1] != maxfreq:
            table = table[:i]
            break
    return table


def find_max_mode(list1) -> float:
    """Return mode in list1, if there are many modes, it will return the biggest
    :param list1: list, mode of each you want to get
    :return
    """
    if not list1:
        return 0
    list_table = _counts(list1)
    len_table = len(list_table)

    if len_table == 1:
        max_mode = statistics.mode(list1)
    else:
        new_list = []
        for i in range(len_table):
            new_list.append(list_table[i][0])
        max_mode = max(new_list)
    return max_mode


def find_average_mode(arr) -> float:
    """Return mode of arr. If there are many modes, it will return mean of them

    :param arr: list, mode of each you want to get
    :return int
    """
    if not arr:
        return 0
    list_table = _counts(arr)
    len_table = len(list_table)
    new_list = []
    for i in range(len_table):
        new_list.append(list_table[i][0])
    return int(statistics.mean(new_list))


def is_profile_closed(target) -> bool:
    """Returns True if target's profile is closed, and False if it is open
    :param target: VK id
    :return True if profile is closed. False if it is not
    """
    r = requests.get("https://api.vk.com/method/users.get", params={
        "v": settings.version,
        "access_token": settings.token,
        "user_ids": target,
        "fields": "is_closed"
    })
    r = r.json()
    print(r)
    try:
        data = r['response'][0]
    except:
        return True
    print(data)
    try:
        return data['is_closed']
    except:
        return True


def get_bdate(target: str) -> str:
    """Return target's birth date
    :param target: VK id
    :return target's birth date
    """
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
        return -1


def get_name(target: str) -> dict:
    """Returns target's name and some other thing like last_name, vk_id and etc.
    :param target: VK id
    :return target's name
    """
    r = requests.get("https://api.vk.com/method/users.get", params={
        "v": settings.version,
        "access_token": settings.token,
        "user_ids": target,
        "fields": "bdate",
        "name_case": "nom"
    })
    try:
        return r.json()['response'][0]
    except KeyError:
        return -1


def get_id_by_domain(target):
    """Get target's id by domain (short link)
    :param target: VK domain
    :return target's ID
    """
    r = requests.get("https://api.vk.com/method/users.get", params={
        "v": settings.version,
        "access_token": settings.token,
        "user_ids": target,
        "fields": "id",
        "name_case": "nom"
    })
    try:
        ret = r.json()['response'][0]['id']
        # print(f"target id: {ret}")
        return ret
    except KeyError:
        pass
    except IndexError:
        pass


def get_friends(target, count=10000):
    """Get target's dict friends or -1 if profile is closed.
    :param target: VK id
    :param count: count of friends you want to get
    :return: dict with target's friends
    """
    all_data = []
    target_id = get_id_by_domain(target)
    r = requests.get("https://api.vk.com/method/friends.get", params={
        "v": settings.version,
        "access_token": settings.token,
        "user_id": target_id,
        "order": "random",
        "count": count,
    })
    r = r.json()
    try:
        data = r['response']['items']
        all_data.extend(data)
    except:
        return -1
    return all_data


def get_age(target):
    """Get target's age
    :param target: VK id
    :return target's age
    """
    birth_date_str = get_bdate(target)
    age = get_age_by_bdate(birth_date_str)
    return age


def get_friends_ages(target):
    """Get target's friends' ages
    :param target: VK id
    :return List with ages or -1 if profile is closed
    """
    friends_bdate = get_friends_bdate(target)
    ages = []
    age = -1
    if friends_bdate == "PC":
        return "PC"
    for person in friends_bdate:
        try:
            age = get_age_by_bdate(person['bdate'])
        except KeyError:
            pass
        if age != -1:
            ages.append(age)
    return ages


def get_friends_bdate(target):
    """Get target's friends' birth dates
    :param target: target
    :return: list with friends' birth dates or -1 if profile is closed
    """
    target_id = get_id_by_domain(target)
    # print(f"target_id: {target_id}")
    r = requests.get("https://api.vk.com/method/friends.get", params={
        "v": settings.version,
        "access_token": settings.token,
        "user_id": target_id,
        "fields": "bdate",
        "count": 10000
    })
    try:
        return r.json()['response']['items']
    except KeyError:
        return "PC"


def get_domain_by_id(target):
    """Get target's domain by id
    :param target: target's id
    :return: target's domain
    """
    r = requests.get("https://api.vk.com/method/users.get", params={
        "v": settings.version,
        "access_token": settings.token,
        "fields": "domain",
        "user_id": target
    })
    # print(r.text)
    try:
        ret = r.json()['response'][0]['domain']
        # print(f"target_domain1sasas: {ret}")
        return ret
    except KeyError:
        return -1
    except IndexError:
        return -1


def get_age_by_bdate(birth_date_str):
    """Get age by birth date. (How many full years passed)
    :param birth_date_str: birth_date (string) Formatted like DD.MM.YYYY
    :return: age
    """
    today_date = datetime.datetime.today()
    if birth_date_str == -1:
        return -1
    length = len(birth_date_str)
    if length < 8:
        return -1
    birth_date_str_list = birth_date_str.split('.')
    birth_day = int(birth_date_str_list[0])
    birth_month = int(birth_date_str_list[1])
    birth_year = int(birth_date_str_list[2])
    try:
        birth_date = datetime.date(birth_year, birth_month, birth_day)
    except ValueError:
        return -1
    age = relativedelta(today_date, birth_date)
    return age.years
