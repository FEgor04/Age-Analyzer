import datetime
import pickle
import statistics as st

import numpy as np
import pandas as pd
import age_analyzer as analyzer
from sklearn import linear_model

import settings


def find_average_mode(arr):
    """"

    :param arr: list, mode of each you want to get
    :return mode. If there are many modes, it will return average of them
    """
    list_table = st._counts(arr)
    len_table = len(list_table)
    new_list = []
    for i in range(len_table):
        new_list.append(list_table[i][0])
    return int(st.mean(new_list))


def log(event, text, file):
    """

    :param event: what happened
    :param text: description
    :param file: where to log
    :return Makes log formatted like this: TIME::EVENT::TEXT. It will put it in file
    """
    if settings.log_needed:
        read = open(file, 'r')
        file_text = read.read()
        read.close()
        now = datetime.datetime.now()
        log_text = f"{now}::{event}::{text}"
        f = open(file, 'w')
        f.write(file_text + log_text + '\n')
    else:
        pass


class NeuralNetwork:
    def __init__(self):
        self.reg = linear_model.LinearRegression()
        log("INIT", f"Model inited.", "log/neuroanalyzer.log")
        pass

    def prepare_data_from_df(self, df):
        """

        :param df: dataframe. Type: pandas.dataframe
        :return: Creates y_train_dict and x_train_dict - pandas.dataframe to train neural network.
        """
        mean_arr_train = []
        hmean_arr_train = []
        mode_arr_train = []
        median_arr_train = []
        std_arr_train = []
        real_age_arr_train = []
        for i in range(len(df)):
            print(df)
            print(df["Mean"][i])
            if df["Mean"][i] != "PROFILE CLOSED":
                mean_arr_train.append(df["Mean"][i])
                hmean_arr_train.append(df["Harmonic Mean"][i])
                mode_arr_train.append(df["Mode"][i])
                median_arr_train.append(df["Median"][i])
                std_arr_train.append(df["std"][i])
                real_age_arr_train.append(df["Real Age"][i])
        self.x_train_dict = {
            "Mean": mean_arr_train,
            "Mode": mode_arr_train,
            "HMean": hmean_arr_train,
            "Median": median_arr_train,
            "std": std_arr_train
        }
        self.y_train_dict = {
            "Real Age": real_age_arr_train
        }
        log("prepare_data_from_df", f"Data prepared successfully. Data length: {len(self.x_train_df)}",
            "log/neuroanalyzer.log")

    def train(self, df):
        """

        :param df: dataframe with input data
        :return: saves model in settings.neuronet_file
        """
        self.prepare_data_from_df(df)
        self.x_train_df = pd.DataFrame(self.x_train_dict)
        self.y_train_df = pd.DataFrame(self.y_train_dict)
        self.reg.fit(self.x_train_df, self.y_train_df)
        log("train", f"Model trained successfully. Data length: {len(self.x_train_df)}",
            "log/neuroanalyzer.log")
        self.save_model(settings.neuronet_file)

    def train_with_raw_data(self, raw_df):
        log("train_with_raw_data", f"train_with_raw_data() started.", "log/neuroanalyzer.log")
        real_age_arr = []
        mean_arr = []
        hmean_arr = []
        mode_arr = []
        median_arr = []
        std_arr = []
        for i in range(raw_df.__len__()):
            id = raw_df['ID'][i]
            ages = (analyzer.get_friends_ages(id))
            if ages != "PC":
                ages = np.array(ages)
                mean_arr.append(round(st.mean(ages)))
                hmean_arr.append(round(st.harmonic_mean(ages)))
                mode_arr.append(find_average_mode(ages))
                median_arr.append(round(st.median(ages)))
                std_arr.append(round(ages.std()))
            else:
                pass
        log("train_with_raw_data", f"Data collected. Started training", "log/neuroanalyzer.log")
        x_train_df = pd.DataFrame(
            {
                "Mean": mean_arr,
                "Mode": mode_arr,
                "Median": median_arr,
                "HMean": hmean_arr,
                "std": std_arr
            }
        )
        y_train_df = pd.DataFrame(
            {
                "Real Age": real_age_arr
            }
        )
        self.reg.fit(x_train_df, y_train_df)
        log("train_with_raw_data", f"Model trained successfully. Data length: {len(x_train_df)}. Saving data",
            "log/neuroanalyzer.log")
        self.save_model(settings.neuronet_file)

    def save_model(self, filename):
        """

        :param filename: file to save model in
        :return: saves model in filename
        """
        pickle.dump(self.reg, open(filename, 'wb'))
        log("save_model", "Model saved successfully", "log/neuroanalyzer.log")

    def open_model(self, filename):
        """

        :param filename: file to open model from
        :return: opens model from filename
        """
        self.reg = pickle.load(open(filename, 'rb'))
        log("open_model", "Model loaded successfully", "log/neuroanalyzer.log")

    def query(self, ages):
        """

        :param ages: list with ages
        :return: estimated age by list with ages
        """
        mean = round(st.mean(ages), 0)
        median = round(st.median(ages), 0)
        hmean = round(st.harmonic_mean(ages), 0)
        mode = round(find_average_mode(ages), 0)
        std = round(np.array(ages).std(), 0)
        predicted = (self.reg.predict([[mean, hmean, mode, median, std]]))
        predicted = round(predicted[0][0], 2)
        log("query",
            f"Predicted successfully. Mean: {mean}. HMean: {hmean}. Mode: {mode}. Median: {median}. Std: {std}."
            f" Result: {predicted}.",
            "log/neuroanalyzer.log")
        self.save_model(filename=settings.neural_network_file)
        return predicted
