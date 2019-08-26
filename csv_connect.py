import age_analyzer as analyzer
import pandas as pd
from math import floor
import statistics as st
import numpy as np
import matplotlib.pyplot as plt


def people_with_open_profile(data):
    count = 0
    for i in range(0, data.__len__()):
        if data["Mean"][i] == "PROFILE CLOSED":
            pass
        else:
            count -= -1
    return count

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
            except TypeError:
                data["Mode"][i] = "PROFILE CLOSED"
            except st.StatisticsError:
                data["Mode"][i] = max(set(ages), key=ages.count)

            try:
                data["Harmonic Mean"][i] = floor(st.harmonic_mean(ages))
            except:
                data["Harmonic Mean"][i] = "PROFILE CLOSED"

            try:
                data["Median"][i] = floor(st.median(ages))
            except:
                data["Median"][i] = "PROFILE CLOSED"

            try:
                if ages == "PC":
                    data["std"][i] = "PROFILE CLOSED"
                else:
                    ages_np = np.array(ages)
                    data["std"][i] = floor(np.std(ages_np))
            except:
                data["std"][i] = "PROFILE CLOSED"

    df = pd.DataFrame(data)
    df.fillna(0)
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
    for i in range(1, 30):
        error_level_list.append(i)
        # print(type(mean_row[i].item()))
        # print(type(accuracy_mean_list[i-1]))
        try:
            accuracy_mean_list.append(mean_row[i].item() + accuracy_mean_list[i-1])
        except:
            accuracy_mean_list.append(accuracy_mean_list[i-1])
        try:
            accuracy_median_list.append(median_row[i].item() + accuracy_median_list[i-1])
        except:
            accuracy_median_list.append(accuracy_median_list[i-1])
        try:
            accurracy_hmean_list.append(hmean_row[i].item() + accurracy_hmean_list[i-1])
        except:
            accurracy_hmean_list.append(accurracy_hmean_list[i-1])
        try:
            accuracy_mode_list.append(mode_row[i].item() + accuracy_mode_list[i-1])
        except:
            accuracy_mode_list.append(accuracy_mode_list[i-1])
    accuracy_dict = {
        "ErrorLevel": error_level_list,
        "Mean": accuracy_mean_list,
        "HMean": accurracy_hmean_list,
        "Mode": accuracy_mode_list,
        "Median": accuracy_median_list
    }
    return pd.DataFrame(data=accuracy_dict)


def prepare_regression_dataset(filled_file, output_file):
    filled_df = pd.read_csv(filled_file)
    mean_list = []
    mode_list = []
    hmean_list = []
    median_list = []
    real_age_list = []
    std_list = []

    for i in range(0, filled_df.__len__()):
        if filled_df["Mean"][i] != "PROFILE CLOSED":
            mean_list.append(filled_df["Mean"][i])
            mode_list.append(filled_df["Mode"][i])
            median_list.append(filled_df["Median"][i])
            hmean_list.append(filled_df["Harmonic Mean"][i])
            real_age_list.append(filled_df["Real Age"][i])
            std_list.append(filled_df["std"][i])
    dict = {
        "RealAge": real_age_list,
        "Median": median_list,
        "std": std_list,
        "Mean": mean_list,
        "Mode": mode_list,
        "HMean": hmean_list
    }
    output_df = pd.DataFrame(data=dict)
    output_df.to_csv(output_file, index=False)

def build_graph(accuracy_data, count):
    plt.plot(accuracy_data["Mean"]/count, label="Ср. Арифметическое")
    plt.plot(accuracy_data["HMean"]/count, label="Ср. Гармоническое")
    plt.plot(accuracy_data["Mode"]/count, label="Мода")
    plt.plot(accuracy_data["Median"]/count, label="Медиана")
    plt.grid(1)
    plt.legend()
    plt.xlabel("j")
    plt.ylabel("A (j)")
    plt.show()


def analyze(input_file):
    data = pd.read_csv(input_file)
    specified_age = people_who_specified_age(data)
    people_with_true_age = people_whose_vk_age_is_equal_to_real_age(data)
    open_profile_count = people_with_open_profile(data)
    print("+---------------------------------------------------------------------------------------+")
    print(f"|Number of people, who specified their age: {specified_age} ({round( (specified_age / data.__len__() * 100), 2 )} %)\t\t\t\t\t|")
    print(f"|Number of people, whose vk age is equal to real age: {people_with_true_age} ({round( (people_with_true_age / data.__len__() * 100), 2)} %)\t\t\t|")
    print(f"|Number of people, whose vk profile is open: {open_profile_count} ({round( open_profile_count / data.__len__() * 100 , 2)} %)\t\t\t\t|")
    print("+---------------------------------------------------------------------------------------+")
    accuracy_data = fill_accuracy(data)
    build_graph(accuracy_data, open_profile_count)
    # print(data)