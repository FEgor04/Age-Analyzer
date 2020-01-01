# -*- coding: utf-8 -*-

import datetime
import math
import statistics

import requests

import settings


def find_max_mode(list1):
    """

    :param list1: list, mode of each you want to get
    :return max_mode. If there are many modes, it will return maximal of them
    """
    list_table = statistics._counts(list1)
    len_table = len(list_table)

    if len_table == 1:
        max_mode = statistics.mode(list1)
    else:
        new_list = []
        for i in range(len_table):
            new_list.append(list_table[i][0])
        max_mode = max(new_list)
    return max_mode


def find_average_mode(arr):
    """

    :param arr: list, mode of each you want to get
    :return mode. If there are many modes, it will return average of them
    """
    list_table = statistics._counts(arr)
    len_table = len(list_table)
    new_list = []
    for i in range(len_table):
        new_list.append(list_table[i][0])
    return int(statistics.mean(new_list))


def is_profile_closed(target):
    """

    :param target: VK id
    :return True if profile is closed. False if it is not
    """
    r = requests.get("https://api.vk.com/method/users.get", params={
        "v": settings.version,
        "access_token": settings.token,
        "user_ids": target,
        "fields": "",
        "name_case": "Nom"
    })
    try:
        data = r.json()['response'][0]
    except:
        return True
    try:
        return not(data['can_access_closed'] or data['is_closed'])
    except:
        return True


def get_bdate(target):
    """

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


def get_name(target):
    """

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
    except:
        return -1


def get_id_by_domain(target):
    """

    :param target: VK domain
    :return target's ID by his domain
    """
    r = requests.get("https://api.vk.com/method/users.get", params={
        "v": settings.version,
        "access_token": settings.token,
        "user_ids": target,
        "fields": "id",
        "name_case": "nom"
    })
    try:
        return r.json()['response'][0]['id']
    except:
        pass


def get_friends(target, count):
    """

    :param target: VK id
    :param count: count of friends you want to get
    :return: dict with target's friends
    """
    all_data = []
    r = requests.get("https://api.vk.com/method/friends.get", params={
        "v": settings.version,
        "access_token": settings.token,
        "user_id": get_id_by_domain(target),
        "order": "name",
        "count": count,
        "fields": "nickname"
    })
    r = r.json()
    try:
        data = r['response']['items']
        all_data.extend(data)
    except:
        return -1
    if count > 5000:
        r = requests.get("https://api.vk.com/method/friends.get", params={
            "v": settings.version,
            "access_token": settings.token,
            "user_id": get_id_by_domain(target),
            "order": "name",
            "count": count - 5000,
            "offset": 5000,
            "fields": "nickname",
            "name_case": "nom"
        })
        r = r.json()
        try:
            data = r['response']['items']
            all_data.extend(data)
        except:
            return -1
    return all_data


def get_age(target):
    """

    :param target: VK id
    :return target's age by his VK id
    """
    birth_date_str = get_bdate(target)
    today_date = datetime.datetime.today()
    if birth_date_str == -1:
        return -1
    length = len(birth_date_str)
    if length < 8:
        return -1
    birth_date_str_list = birth_date_str.split('.')
    birth_year = int(birth_date_str_list[3])
    birth_month = int(birth_date_str_list[1])
    birth_day = int(birth_date_str_list[0])
    birth_date = datetime.date(birth_year, birth_month, birth_day)
    age = today_date.toordinal() - birth_date.toordinal()
    age = age - age / 366
    age = math.floor(age / 365)
    return age


def get_friends_ages(target):
    """

    :param target: VK id
    :return friend's ages
    """
    friends_bdate = get_friends_bdate(target)
    ages = []
    age = -1
    if friends_bdate == "PC":
        return "PC"
    for person in friends_bdate:
        try:
            age = get_age_by_bdate(person['bdate'])
        except:
            pass
        if age != -1:
            ages.append(age)
    return ages


def get_friends_bdate(target):
    """

    :param target: friends' birth dates
    :return:
    """
    target_id = get_id_by_domain(target)
    r = requests.get("https://api.vk.com/method/friends.get", params={
        "v": settings.version,
        "access_token": settings.token,
        "user_id": target_id,
        "order": "name",
        "fields": "bdate",
        "name_case": "nom",
        "count": "10000"
    })
    try:
        return r.json()['response']['items']
    except KeyError:
        return "PC"


def get_age_by_bdate(birth_date_str):
    """

    :param birth_date_str: birth_date (string) it is like DD.MM.YYYY
    :return: age
    """
    today_date = datetime.datetime.today()
    if birth_date_str == -1:
        return -1
    length = len(birth_date_str)
    if length < 8:
        return -1
    birth_date_str_list = birth_date_str.split('.')
    birth_year = int(birth_date_str_list[3])
    birth_month = int(birth_date_str_list[1])
    birth_day = int(birth_date_str_list[0])
    birth_date = datetime.date(birth_year, birth_month, birth_day)
    age = today_date.toordinal() - birth_date.toordinal()
    age = age - age / 366
    age = math.floor(age / 365)
    return age
