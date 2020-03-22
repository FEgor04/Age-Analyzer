import statistics as st

import numpy as np
import pandas as pd

import age_analyzer as analyzer


def people_with_open_profile(data: pd.DataFrame):
    """
    Finds count of people with open profile
    :param data: pandas.DataFrame with needed cells
    :return: count of people whose profile is open
    """
    count = data[data["Mean"] != -1]["ID"].count()
    return count


def find_average_mode(arr):
    """
    Finds average mode of arr
    :param arr: list, mode of each you want to get
    :return mode. If there are many modes, it will return average of them
    """
    list_table = st._counts(arr)
    len_table = len(list_table)
    new_list = []
    for i in range(len_table):
        new_list.append(list_table[i][0])
    return int(st.mean(new_list))


def fill_vk_age(data: pd.DataFrame):
    """
    Fills VK Age in output_csv file
    :param data:
    """
    for i in range(0, data.__len__()):
        target = data['ID'][i]
        if analyzer.get_age(target) != -1:
            data["VK Age"][i] = analyzer.get_age(target)
        else:
            data["VK Age"][i] = "-1"
    return data


def fill_friends_age(data: pd.DataFrame):
    """

    Function fills friends ages' Mean, Median, etc.

    :param data: pd.DataFrame, raw data
    """
    for i in range(0, len(data)):
        if analyzer.is_profile_closed(data['ID'][int(i)]):
            print(f"{data['ID'][i]} is closed")
            pass
        else:
            ages = analyzer.get_friends_ages(data["ID"][i])
            print(f"ID: {data['ID'][i]}. Ages: {ages} ")
            data["Mean"][i] = round(st.mean(ages), 2)
            data["Mode"][i] = round(find_average_mode(ages), 2)
            data["Harmonic Mean"][i] = round(st.harmonic_mean(ages), 2)
            data["Median"][i] = round(st.median(ages), 2)
            ages_np = np.array(ages)
            data["std"][i] = round(np.std(ages_np), 2)
    df = pd.DataFrame(data)
    return df


def people_who_specified_age(data: pd.DataFrame):
    """
    Finds count of people who specified their age in VK
    :param data: pandas.DataFrame with needed cells
    :return: Count of people who specify their age
    """
    count = data[data["VK Age"] != -1]["ID"].count()
    return count


def people_whose_vk_age_is_equal_to_real_age(data: pd.DataFrame):
    """
    Find count of people whose real age if equal to VK age
    :param data: pandas.DataFrame with needed cells
    :return: Count of people whose VK age is equal to Real Age
    """
    count = data[data["VK Age"] == data["Real Age"]]["ID"].count()
    return count



