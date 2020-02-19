import datetime
import statistics as st
import numpy as np
import logging
import pandas as pd
import matplotlib.pyplot as plt
import telebot
import age_analyzer
import neuroanalyzer
import settings
from neuroanalyzer import NeuralNetwork

bot = telebot.TeleBot(settings.tg_api)
neural_network: NeuralNetwork = neuroanalyzer.NeuralNetwork()


def counts_by_arr(arr: np.ndarray) -> np.ndarray:
    """

    This fucntion returns array with count of each element.
    A[j] = count of j meetings in input
    :param arr: List
    :return:
    """
    answ_arr = list([0] * (max(arr) + 1))
    for i in arr:
        answ_arr[i] += 1
    return np.array(answ_arr)


def launch():
    """
        This function launches bot
    """
    try:
        neural_network.open_model(settings.neural_network_file)
    except:
        neural_network.train_with_raw_data(pd.read_csv(settings.project_folder + '/' + settings.csv_file))
    logging.basicConfig(format=u'%(filename)s,%(lineno),%(levelname)s,%(asctime)s,%(message)s',
                        level=logging.INFO, filename=settings.project_folder + '/' + 'log/log.csv')
    logging.info("launch,Bot launched.")
    bot.polling()


def find_max_mode(list1):
    """

    This function finds maximal mode in list1

    :param list1: list, mode of each you want to get
    :return max_mode. If there are many modes, it will return maximal of them
    """
    list_table = st._counts(list1)
    len_table = len(list_table)

    if len_table == 1:
        max_mode = st.mode(list1)
    else:
        new_list = []
        for i in range(len_table):
            new_list.append(list_table[i][0])
        max_mode = max(new_list)
    return max_mode


def find_average_mode(arr):
    """

    This function finds average mode in arr

    :param arr: list, mode of each you want to get
    :return mode. If there are many modes, it will return average of them
    """
    list_table = st._counts(arr)
    len_table = len(list_table)
    new_list = []
    for i in range(len_table):
        new_list.append(list_table[i][0])
    return int(st.mean(new_list))


@bot.message_handler(commands=['analyze'])
def answer(message):
    by = f"{message.chat.first_name} {message.chat.last_name} ({message.chat.id})"
    try:
        to_build = (message.text.split(' '))[1]
    except:
        try:
            logging.info(f"analyze_response,Wrong format. Requested by {by}")
        except:
            logging.error(f"analyze_error")
        bot.send_message(message.chat.id, "Введите по формату\n"
                                          "/analyze {id}")
    try:
        logging.info(f"analyze_request,{by} wants to analyze {to_build}".encode("ascii", errors='xmlcharrefreplace'))
    except:
        logging.error(f"analyze_error")
    ages = age_analyzer.get_friends_ages(to_build)
    if age_analyzer.is_profile_closed(to_build) or ages == "PC":
        logging.info(f"analyze_response,{to_build} - no profile. Requested by {by}")
        bot.send_message(message.chat.id, "Страница закрыта или не существует. Попробуйте еще раз.")
    else:
        bot.send_message(message.chat.id, f"Мы начали анализировать {to_build}")
        logging.info(f"analyze_analyzing,Started analyze {to_build}. Requested by {by}.")
        target_name = age_analyzer.get_name(to_build)
        target_age = age_analyzer.get_age(to_build)
        if target_age == -1:
            target_age = "не указан"
        friends_ages = age_analyzer.get_friends_ages(to_build)
        predicted = (neural_network.query(friends_ages))
        mode = find_max_mode(friends_ages)
        response = f"Мы проанализировали {target_name['first_name']} {target_name['last_name']}\n" \
                   f"Возраст, указанный в профиле - {target_age}.\n" \
                   f"Однако, мы полагаем, что настоящий возраст: {predicted} \n" \
                   f"Мода: {mode}"

        bot.send_message(message.chat.id, response)
        logging.info(f"analyze_response,Answered to {by}. Request: {message.chat.id}")


@bot.message_handler(commands=["histogram"])
def build_histogram(message):
    by = f"{message.chat.first_name} {message.chat.last_name} ({message.chat.id})"
    try:
        to_build = (message.text.split(' '))[1]
    except:
        logging.info(f"histogram_response,Wrong format. Requested by {by}")
        bot.send_message(message.chat.id, "Введите по формату\n"
                                          "/analyze {id}")
        return
    logging.info(f"histogram_request,{by} wants to build histogram {to_build}")
    ages = age_analyzer.get_friends_ages(to_build)
    if age_analyzer.is_profile_closed(to_build) or ages == "PC":
        logging.info(f"histogram_response,{to_build} - no profile. Requested by {by}")
        bot.send_message(message.chat.id, "Страница закрыта или не существует. Попробуйте еще раз.")
    else:
        bot.send_message(message.chat.id, f"Мы начали анализировать {to_build}")
        logging.info(f"histogram_start,Started analyze {to_build} to build histogram. Requested by {by}")
        target_name = age_analyzer.get_name(to_build)
        ages = age_analyzer.get_friends_ages(target=to_build)
        y = counts_by_arr(ages)
        x = range(len(y))
        plt.figure(figsize=(15, 5), dpi=80)
        plt.bar(x=x, height=y)
        plt.xlim(min(ages) - 5, max(ages) + 5)
        plt.ylim(0, max(y) + 5)
        plt.yticks(np.arange(0, max(y) + 5, 5))
        plt.xticks(np.arange(min(ages), max(ages), 5))
        plt.title(f"{target_name['first_name']} {target_name['last_name']}", fontsize=24)
        plt.ylabel("Count", fontsize=16)
        plt.xlabel("Age", fontsize=16)
        plt.savefig(f"{settings.project_folder}/graph/{to_build}.png")
        photo = open(f"{settings.project_folder}/graph/{to_build}.png", 'rb')
        logging.info("histogram_response,Histogram built. Sending it back.")
        bot.send_message(message.chat.id,
                         f"Мы построили гистограмму возрастов друзей"
                         f" пользователя {target_name['first_name']} {target_name['last_name']}.")
        bot.send_chat_action(message.chat.id, 'upload_photo')
        bot.send_photo(message.chat.id, photo)
        plt.close()
        photo.close()
