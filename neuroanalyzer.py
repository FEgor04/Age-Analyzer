import logging
import statistics as st

import catboost
import numpy as np
import pandas as pd

import postgres_report
import settings
from age_analyzer import _counts


def find_average_mode(arr):
    """Return average mode in arr
    :param arr: list, mode of each you want to get
    :return mode. If there are many modes, it will return average of them
    """
    list_table = _counts(arr)
    len_table = len(list_table)
    new_list = []
    for i in range(len_table):
        new_list.append(list_table[i][0])
    return int(st.mean(new_list))


def find_std(arr):
    """Return std in arr
    :param arr: array
    :return std
    """
    std = np.array(arr).std()
    return std


class AgeRegressor:
    """Class for catboost.CatBoostRegressor
    """

    def __init__(self):
        """Initiate AgeRegressor
        """
        self.reg = catboost.CatBoostRegressor(learning_rate=0.5, depth=2, loss_function='RMSE', iterations=1000)
        if settings.log_needed:
            handler = logging.FileHandler(filename=settings.project_folder + '/log/log.csv', mode='a')
            logging.basicConfig(format='%(asctime)s^%(name)s^%(levelname)s^%(message)s',
                                level=logging.INFO, handlers=[handler])
            logging.info("INIT^Model initiated.")

    def train_with_raw_data(self, df_raw: pd.DataFrame, from_table=False):
        """Train catboost.CatBoostRegressor model with raw data
        :param df_raw: df filled with csv_connect.fill_vk_age and csv_connect.fill_friends_age
        :return:
        """
        if from_table:
            df_raw = postgres_report.get_df_to_train()
        if settings.log_needed:
            logging.info("train_with_raw_data^Started training.")
        # print(df_raw)
        df_raw.fillna(-1.0, inplace=True)
        df_filtered = df_raw[df_raw['Mean'] != -1]
        train_columns = ['Mean', 'Harmonic Mean', 'Mode', 'Median', 'std', 'Friends Count']
        x_train_df = df_filtered[train_columns]
        y_train_df = df_filtered['Real Age']
        if settings.log_needed:
            logging.info("train_with_raw_data^Data collected. Starting training.")
        self.reg.fit(x_train_df, y_train_df, verbose=False)
        if settings.log_needed:
            logging.info(f"train_with_raw_data^Catboost Regressor fitted successfully."
                         f"Tree Count: {self.reg.tree_count_}. Saving data.")
        self.save_model(settings.neural_network_file)

    def save_model(self, filename):
        """Save AgeRegressor model
        :param filename: file to save model in
        :return: saves model in filename
        """
        self.reg.save_model(filename)
        if settings.log_needed:
            logging.info("save_model^Model saved successfully.")

    def open_model(self, filename):
        """Open AgeRegressor model
        :param filename: file to open model from
        :return:
        """
        self.reg = catboost.CatBoostRegressor(learning_rate=0.5, depth=2, loss_function='RMSE',
                                              iterations=1000)
        self.reg.load_model(filename)
        if settings.log_needed:
            logging.info(f"open_model^Model loaded successfully. Tree Count: {self.reg.tree_count_}")

    def _query(self, ages, save: bool = True, log: bool = True) -> float:
        """Query to catboost model
        :param ages: list with ages
        :param save: Need to save model or not
        :param log: Need to log or not
        :return: estimated age by list with ages
        """
        mean = round(st.mean(ages), 2)
        median = round(st.median(ages), 2)
        hmean = round(st.harmonic_mean(ages), 2)
        mode = round(find_average_mode(ages), 2)
        std = round(np.array(ages).std(), 2)
        friends_cnt = len(ages)
        predicted = self.reg.predict([mean, hmean, mode, median, std, friends_cnt])
        predicted = round(predicted, 2)
        if log and settings.log_needed:
            logging.info(
                f"query^Predicted successfully. Mean: {mean}. HMean: {hmean}. Mode: {mode}. Median: {median}. Std: {std}. Result: {predicted}."
            )
        if save:
            self.save_model(filename=settings.neural_network_file)
        return predicted

    def query(self, domain, save=True, log=True):
        return postgres_report.analyze_and_insert(domain, self)