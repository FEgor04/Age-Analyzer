import datetime
import pickle
import logging
import statistics as st
import numpy as np
import pandas as pd
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


class NeuralNetwork:
    def __init__(self):
        self.reg = linear_model.LinearRegression()
        logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d],%(levelname)-8s [%(asctime)s],%(message)s',
                            level=logging.INFO, filename=settings.project_folder + '/' + 'log/log.csv')
        logging.info("INIT,Model initiated.")
        pass

    def train_with_raw_data(self, df_raw: pd.DataFrame):
        logging.info("train_with_raw_data,Started training.")
        df_raw.fillna(-1.0, inplace=True)
        real_age_list = []
        mean_list = []
        hmean_list = []
        median_list = []
        mode_list = []
        std_list = []
        for i in range(df_raw.__len__()):
            if df_raw['Mean'][i] != -1:
                real_age_list.append(df_raw['Real Age'][i])
                mean_list.append(df_raw['Mean'][i])
                hmean_list.append(df_raw['Harmonic Mean'][i])
                mode_list.append(df_raw['Mode'][i])
                median_list.append(df_raw['Median'][i])
                std_list.append(df_raw['std'][i])
        logging.info("train_with_raw_data,Data collected. Starting training.")
        y_train_df = pd.DataFrame({
            "Real Age": real_age_list
        })
        x_train_df = pd.DataFrame({
            'Mean': mean_list,
            'Harmonic Mean': hmean_list,
            'Mode': mode_list,
            'Median': median_list,
            'std': std_list
        })
        self.reg.fit(x_train_df, y_train_df)
        logging.info(f"train_with_raw_data,Model trained successfully. Data length: {len(x_train_df)}. Saving data.")
        self.save_model(settings.neural_network_file)

    def save_model(self, filename):
        """

        :param filename: file to save model in
        :return: saves model in filename
        """
        pickle.dump(self.reg, open(filename, 'wb'))
        logging.info("save_model,Model saved successfully.")

    def open_model(self, filename):
        """

        :param filename: file to open model from
        :return: opens model from filename
        """
        self.reg = pickle.load(open(filename, 'rb'))
        logging.info("open_model,Model loaded successfully.")

    def query(self, ages):
        """

        :param ages: list with ages
        :return: estimated age by list with ages
        """
        mean = round(st.mean(ages), 2)
        median = round(st.median(ages), 2)
        hmean = round(st.harmonic_mean(ages), 2)
        mode = round(find_average_mode(ages), 2)
        std = round(np.array(ages).std(), 2)
        predicted = self.reg.predict([[mean, hmean, mode, median, std]])
        predicted = round(predicted[0][0], 2)
        logging.info(
            f"query,Predicted successfully. Mean: {mean}. HMean: {hmean}. Mode: {mode}. Median: {median}. Std: {std}. Result: {predicted}."
        )
        self.save_model(filename=settings.neural_network_file)
        return predicted
