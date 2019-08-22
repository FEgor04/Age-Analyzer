import age_analyzer as analyzer
import pandas as pd
from math import floor
import statistics as st
import numpy as np

def fill_vk_age(input_csv, output_csv):
    data = pd.read_csv(input_csv)
    for i in range(0, data.__len__()):
        target = data['ID'][i]
        if analyzer.get_age(target) != -1:
            data["VK Age"][i] = analyzer.get_age(target)
        else:
            data["VK Age"][i] = "IS NOT SPECIFIED"
    df = pd.DataFrame(data)
    df.to_csv(output_csv)

def fill_friends_age(input_csv, output_csv):
    data = pd.read_csv(input_csv)
    for i in range(0, data.__len__()):
        if analyzer.is_profile_closed(data["ID"][i]):
            print(f"{data['ID'][i]} is closed")
            pass
        else:
            ages = analyzer.get_friends_ages(data["ID"][i])
            try:
                data["Mean"][i] = floor(st.mean(ages))
            except:
                data["Mean"][i] = "PROFILE CLOSED"

            try:
                data["Mode"][i] = floor(st.mode(ages))
            except:
                data["Mode"][i] = "PROFILE CLOSED"

            try:
                data["Harmonic Mean"][i] = floor(st.harmonic_mean(ages))
            except:
                data["Harmonic Mean"][i] = "PROFILE CLOSED"

            try:
                data["Median"][i] = floor(st.median(ages))
            except:
                data["Median"][i] = "PROFILE CLOSED"

    df = pd.DataFrame(data)
    print(df)
    df.to_csv(output_csv, index=False)

def people_who_specified_age(data):
    count  = 0
    for i in range(0, data.__len__()):
        if data["VK Age"][i] != "IS NOT SPECIFIED":
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
    columns = ['Mean', 'HMean', 'Median', 'Mode']
    error_list_dict = {
        'Mean': [],
        'HMean': [],
        'Median': [],
        'Mode': []
    }
    # print(type(columns))
    # print(columns)
    # print(error_list_data)
    for i in range(0, data.__len__()):
        if data["Mean"][i] != "PROFILE CLOSED" and data["Mode"][i] != "PROFILE CLOSED" and data["Median"][i] != "PROFILE CLOSED" and data["Harmonic Mean"][i] != "PROFILE CLOSED":
            mean_error = abs(int(data["Mean"][i]) - int(data["Real Age"][i]))
            hmean_error = abs(int(data["Harmonic Mean"][i]) - int(data["Real Age"][i]))
            median_error = abs(int(data["Median"][i]) - int(data["Real Age"][i]))
            mode_error = abs(int(data["Mode"][i]) - int(data["Real Age"][i]))
            error_list_dict["Mean"].append(mean_error)
            error_list_dict["HMean"].append(hmean_error)
            error_list_dict["Median"].append(median_error)
            error_list_dict["Mode"].append(mode_error)
        else:
            pass
    error_list_data = pd.DataFrame(data=error_list_dict)
    return error_list_data

def fill_accuracy(data):
    print(f"Data type: {type(data)}", end="\n\n")
    error_data = fill_error_list(data)
    mean_row = error_data["Mean"].value_counts()
    hmean_row = error_data["HMean"].value_counts()
    median_row = error_data["Median"].value_counts()
    mode_row = error_data["Mode"].value_counts()

    error_level_list = [0]
    accuracy_mean_list = [mean_row[0].item()]
    accurracy_hmean_list = [hmean_row[0].item()]
    accuracy_mode_list = [mode_row[0].item()]
    accuracy_median_list = [median_row[0].item()]
    for i in range(1, data.__len__()):
        error_level_list.append(i)
        accuracy_mean_list.append(mean_row[i].item() + accuracy_mean_list[i-1])
        accuracy_mode_list.append(mean_row[i].item() + accuracy_mode_list[i-1])
        accuracy_median_list.append(mean_row[i].item() + accuracy_median_list[i-1])
        accurracy_hmean_list.append(mean_row[i].item() + accurracy_hmean_list[i-1])
    accuracy_dict = {
        "ErrorLevel": error_level_list,
        "Mean": accuracy_mean_list,
        "HMean": accurracy_hmean_list,
        "Mode": accuracy_mode_list,
        "Median": accuracy_median_list
    }
    return pd.DataFrame(data=accuracy_dict)

def analyze(input_file):
    data = pd.read_csv(input_file)
    specified_age = people_who_specified_age(data)
    people_with_true_age = people_whose_vk_age_is_equal_to_real_age(data)
    print(f"Number of people, who specified their age: {specified_age} ({round( (specified_age / data.__len__() * 100), 2 )} %)")
    print(f"Number of people, whose vk age is equal to real age: {people_with_true_age} ({round( (people_with_true_age / data.__len__() * 100), 2)} %)")
    print("-------------------------------------------------------------------------------------")
    # print(data)
    # error_list_data = fill_error_list(data)
    # print(error_list_data["Mean"]
    # print(error_list_data["Mean"].value_counts()[2])
    accuracy_data = fill_accuracy(data)
    print(accuracy_data)
    # print(data)