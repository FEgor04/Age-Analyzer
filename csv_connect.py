import statistics as st
import numpy as np
import pandas as pd

import age_analyzer as analyzer


def people_with_open_profile(data):
    count = 0
    for i in range(0, data.__len__()):
        if data["Mean"][i] == -1:
            pass
        else:
            count -= -1
    return count


def find_average_mode(arr):
    list_table = st._counts(arr)
    len_table = len(list_table)
    new_list = []
    for i in range(len_table):
        new_list.append(list_table[i][0])
    return int(st.mean(new_list))


def fill_vk_age(input_csv, output_csv):
    data = pd.read_csv(input_csv)
    for i in range(0, data.__len__()):
        target = data['ID'][i]
        if analyzer.get_age(target) != -1:
            data["VK Age"][i] = analyzer.get_age(target)
        else:
            data["VK Age"][i] = "-1"
    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)


def fill_friends_age(input_csv, output_csv):
    data = pd.read_csv(input_csv)
    for i in range(0, data.__len__()):
        if analyzer.is_profile_closed(data["ID"][i]):
            print(f"{data['ID'][i]} is closed")
            pass
        else:
            ages = analyzer.get_friends_ages(data["ID"][i])
            print(f"ID: {data['ID'][i]}. Ages: {ages} ")
            try:
                data["Mean"][i] = round(st.mean(ages), 2)
            except:
                data["Mean"][i] = -1

            try:
                data["Mode"][i] = round(find_average_mode(ages), 2)
            except TypeError:
                data["Mode"][i] = -1

            try:
                data["Harmonic Mean"][i] = round(st.harmonic_mean(ages), 2)
            except:
                data["Harmonic Mean"][i] = -1

            try:
                data["Median"][i] = round(st.median(ages), 2)
            except:
                data["Median"][i] = -1

            try:
                if ages == "PC":
                    data["std"][i] = -1
                else:
                    ages_np = np.array(ages)
                    data["std"][i] = round(np.std(ages_np), 2)
            except:
                data["std"][i] = -1

    df = pd.DataFrame(data)
    print(df)

    df.to_csv(output_csv, index=False)






def people_who_specified_age(data):
    count = 0
    for i in range(0, data.__len__()):
        if data["VK Age"][i] != "-1":
            count += 1
    return count


def people_whose_vk_age_is_equal_to_real_age(data):
    count = 0
    for i in range(0, data.__len__()):
        try:
            if int(data["VK Age"][i]) == int(data["Real Age"][i]):
                count += 1
        except:
            pass
    return count


def fill_error_list(data):
    error_list_dict = {
        'Mean': [],
        'HMean': [],
        'Median': [],
        'Mode': []
    }
    print(data)
    for i in range(0, data.__len__()):
        real_age = int(data["Real Age"][i])
        if data["Mean"][i] != -1:
            mean_error = abs(int(data["Mean"][i]) - real_age)
            hmean_error = abs(int(data["Harmonic Mean"][i]) - real_age)
            median_error = abs(int(data["Median"][i]) - real_age)
            mode_error = abs(int(data["Mode"][i]) - real_age)
            error_list_dict["Mean"].append(mean_error)
            error_list_dict["HMean"].append(hmean_error)
            error_list_dict["Median"].append(median_error)
            error_list_dict["Mode"].append(mode_error)
        else:
            pass
    error_list_data = pd.DataFrame(data=error_list_dict)
    return error_list_data


def analyze(input_file):
    data = pd.read_csv(input_file)
    specified_age = people_who_specified_age(data)
    people_with_true_age = people_whose_vk_age_is_equal_to_real_age(data)
    open_profile_count = people_with_open_profile(data)
    print("+---------------------------------------------------------------------------------------+")
    print(f"|Number of people, who specified their age: "
          f"{specified_age} ({round((specified_age / data.__len__() * 100), 2)} %)\t\t\t\t\t|")
    print(f"|Number of people, whose vk age is equal to real age: "
          f"{people_with_true_age} ({round((people_with_true_age / data.__len__() * 100), 2)} %)\t\t\t|")
    print(f"|Number of people, whose vk profile is open: "
          f"{open_profile_count} ({round(open_profile_count / data.__len__() * 100, 2)} %)\t\t\t\t|")
    print("+---------------------------------------------------------------------------------------+")
    print(data)
