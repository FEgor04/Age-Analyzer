import statistics as st

import pandas as pd

import age_analyzer
import csv_connect
import neuroanalyzer
import postgres_report
import recursive_estimate
import settings
import tg as telegram_bot
from age_analyzer import _counts


def find_average_mode(arr) -> float:
    """Return mode of arr. If there are many modes, it will return mean of them

    :param arr: list, mode of each you want to get
    :return int
    """
    list_table = _counts(arr)
    len_table = len(list_table)
    new_list = []
    for i in range(len_table):
        new_list.append(list_table[i][0])
    return int(st.mean(new_list))


if __name__ == "__main__":
    ANALYZE = True  # Set it by yourself
    BOT = False
    FILL_CSV = False
    TRAIN_MODEL = False
    TRAIN_MODEL_WITH_TABLE = False
    FILL_TABLE = False
    FILL_TABLE_RECURSIVE = False
    if FILL_CSV:
        df = pd.read_csv('age_research.csv')
        df = csv_connect.fill_friends_age(df)
        df = csv_connect.fill_vk_age(df)
        df.fillna(-1.0, inplace=True)
        df.to_csv('age_research1.csv', index=False)
    if TRAIN_MODEL:
        model = neuroanalyzer.AgeRegressor()
        if not TRAIN_MODEL_WITH_TABLE:
            df = pd.read_csv('age_research1.csv')
            model.train_with_raw_data(df, False)
        else:
            model.train_with_raw_data([], True)
        model.save_model('neuronet.sav')
    if FILL_TABLE:
        df = pd.read_csv('age_research1.csv')
        model = neuroanalyzer.AgeRegressor()
        model.open_model('neuronet.sav')
        for i in range(len(df)):
            now_target = df['ID'][i]
            try:
                model.query(now_target, False, False)
                postgres_report.set_real_age(now_target, df['Real Age'][i], True)
            except:
                print("Profile closed.")
                pass
    if FILL_TABLE_RECURSIVE:
        df = pd.read_csv('age_research1.csv')
        model = neuroanalyzer.AgeRegressor()
        model.open_model('neuronet.sav')
        for i in range(len(df)):
            now_target = df['ID'][i]
            if i == 0:
                print("Starting analyzing")
            else:
                print(f"{(i / len(df) * 100):2f}% done.")
            print(f"Current target: {now_target}")
            recursive_estimate.estimate_age_recursive(now_target, model, 3)
    if ANALYZE:
        print("Input target's ID:", end=" ")
        target = input()
        # neural_network.train_with_raw_data(df_with_data)
        # File should be formatted like:
        # ID,Real Age,VK Age,Mean,Harmonic Mean,Mode,Median,std'
        # OR:
        # Bot loads neural network from file
        model = neuroanalyzer.AgeRegressor()
        model.open_model(settings.neural_network_file)
        name = age_analyzer.get_name(target=target)
        predicted = recursive_estimate.estimate_age_recursive(target, model)
        answer = f"Neural network thinks that {name['first_name']} {name['last_name']}" \
                 f"({target}) age is {predicted}"
        print(answer)
    elif BOT:
        telegram_bot.launch()
