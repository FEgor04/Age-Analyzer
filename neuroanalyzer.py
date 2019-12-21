import datetime
import pickle
import statistics as st

import numpy as np
import pandas as pd
from sklearn import linear_model

import settings


def find_average_mode(arr):
    list_table = st._counts(arr)
    len_table = len(list_table)
    new_list = []
    for i in range(len_table):
        new_list.append(list_table[i][0])
    return int(st.mean(new_list))


def log(event, text, file):
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
        log("DATA PREPARED", f"Data prepared successfully. Data length: {len(self.x_train_df)}",
            "log/neuroanalyzer.log")

    def train(self, df):
        self.prepare_data_from_df(df)
        self.x_train_df = pd.DataFrame(self.x_train_dict)
        self.y_train_df = pd.DataFrame(self.y_train_dict)
        self.reg.fit(self.x_train_df, self.y_train_df)
        log("MODEL TRAINED", f"Model trained successfully. Data length: {len(self.x_train_df)}",
            "log/neuroanalyzer.log")
        self.save_model(settings.neuronet_file)

    def save_model(self, filename):
        pickle.dump(self.reg, open(filename, 'wb'))
        log("MODEL SAVED", "Model saved successfully", "log/neuroanalyzer.log")

    def open_model(self, filename):
        self.reg = pickle.load(open(filename, 'rb'))
        log("MODEL LOADED", "Model loaded successfully", "log/neuroanalyzer.log")

    def query(self, ages):
        mean = round(st.mean(ages), 0)
        median = round(st.median(ages), 0)
        hmean = round(st.harmonic_mean(ages), 0)
        mode = round(find_average_mode(ages), 0)
        std = round(np.array(ages).std(), 0)
        predicted = (self.reg.predict([[mean, hmean, mode, median, std]]))
        predicted = round(predicted[0][0], 2)
        # print(f"\n\n\npredicted: {predicted} \n\n\n")
        log("QUERY",
            f"Predicted successfully. Mean: {mean}. HMean: {hmean}. Mode: {mode}. Median: {median}. Std: {std}."
            f" Result: {predicted}.",
            "log/neuroanalyzer.log")
        self.save_model(self=self, filename=settings.neural_network_file)
        return predicted
