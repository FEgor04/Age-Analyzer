import age_analyzer
import neuroanalyzer
import settings
import tg as telegram_bot
import csv_connect
import statistics as st
import numpy as np
import pandas as pd


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


if __name__ == "__main__":
    if settings.analyze:
        print("Input target's ID:", end=" ")
        target = input()
        neural_network = neuroanalyzer.NeuralNetwork()
        # neural_network.train_with_raw_data(df_with_data)
        # File should be formatted like:
        # ID,Real Age,VK Age,Mean,Harmonic Mean,Mode,Median,std'
        # OR:
        # Bot loads neural network from file
        neural_network.open_model(settings.neural_network_file)
        ages = age_analyzer.get_friends_ages(target=target)
        name = age_analyzer.get_name(target=target)
        try:
            predicted = neural_network.query(ages)
            answer = f"Neural network thinks that {name['first_name']} {name['last_name']}" \
                     f"({target}) age is {predicted}"
        except:
            answer = "Profile closed"
        pass
    else:
        telegram_bot.launch()
