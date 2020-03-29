import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import telebot

import age_analyzer
import neuroanalyzer
import settings
from age_analyzer import find_max_mode
from neuroanalyzer import AgeRegressor

bot = telebot.TeleBot(settings.tg_api)
neural_network: AgeRegressor = neuroanalyzer.AgeRegressor()


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


def estimate_age_recursive(target, model=neural_network):
    target_friends = age_analyzer.get_friends(target)
    target_id = age_analyzer.get_id_by_domain(target)
    estimated_ages = []
    if isinstance(target_friends, int):
        return -1  # Profile closed
    for now in target_friends:
        now_ages = age_analyzer.get_friends_ages(now)
        if isinstance(now_ages, list) and now != target_id:
            if len(now_ages) != 0:
                estimated_ages.append(model.query(now_ages, False, False))
    answer = model.query(estimated_ages)
    return answer


def launch():
    """This function launches bot
    """
    try:
        neural_network.open_model(settings.neural_network_file)
    except:
        neural_network.train_with_raw_data(pd.read_csv(settings.project_folder + '/' + settings.csv_file))
    logging.basicConfig(format='%(asctime)s^%(name)s^%(levelname)s^%(message)s',
                        level=logging.INFO, filename=settings.project_folder + '/' + 'log/log.csv')
    logging.info("launch^Bot launched.")
    bot.polling()


@bot.message_handler(commands=['recursive'])
def analyze_recursive(message):
    by = f"{message.chat.first_name} {message.chat.last_name} ({message.chat.id})"
    try:
        target = (message.text.split(' '))[1]
    except:
        logging.info(f"recursive_response^Wrong format. Requested by {by}")
        logging.error(f"recursive_error")
        bot.send_message(message.chat.id, "Введите по формату\n"
                                          "/analyze {id}")
        return
    logging.info(f"recursive_request^{by} wants to analyze {target}".encode("ascii", errors='xmlcharrefreplace'))
    ages = age_analyzer.get_friends_ages(target)
    if age_analyzer.is_profile_closed(target) or ages == "PC":
        logging.info(f"recursive_response^{target} - no profile. Requested by {by}")
        bot.send_message(message.chat.id, "Страница закрыта или не существует. Попробуйте еще раз.")
    else:
        bot.send_message(message.chat.id, f"Мы начали анализировать {target}")
        logging.info(f"recursive_analyzing^Started analyze {target}. Requested by {by}.")
        target_name = age_analyzer.get_name(target)
        target_age = age_analyzer.get_age(target)
        if target_age == -1:
            target_age = "не указан"
        predicted_recursive = estimate_age_recursive(target)
        predicted = neural_network.query(ages)
        response = f"Мы проанализировали {target_name['first_name']} {target_name['last_name']}\n" \
                   f"Возраст, указанный в профиле - {target_age}.\n" \
                   f"Однако, оценив возраст рекурсивно, мы полагаем, что настоящий возраст: {predicted_recursive} \n" \
                   f"При стандартном способе оценки: {predicted}"
        bot.send_message(message.chat.id, response)
        logging.info(f"analyze_response^Answered to {by}. Request: {message.chat.id}")


@bot.message_handler(commands=['analyze'])
def analyze(message):
    by = f"{message.chat.first_name} {message.chat.last_name} ({message.chat.id})"
    try:
        target = (message.text.split(' '))[1]
    except:
        logging.info(f"analyze_response^Wrong format. Requested by {by}")
        logging.error(f"analyze_error")
        bot.send_message(message.chat.id, "Введите по формату\n"
                                          "/analyze {id}")
        return
    logging.info(f"analyze_request^{by} wants to analyze {target}".encode("ascii", errors='xmlcharrefreplace'))
    ages = age_analyzer.get_friends_ages(target)
    if age_analyzer.is_profile_closed(target) or ages == "PC":
        logging.info(f"analyze_response^{target} - no profile. Requested by {by}")
        bot.send_message(message.chat.id, "Страница закрыта или не существует. Попробуйте еще раз.")
    else:
        bot.send_message(message.chat.id, f"Мы начали анализировать {target}")
        logging.info(f"analyze_analyzing^Started analyze {target}. Requested by {by}.")
        target_name = age_analyzer.get_name(target)
        target_age = age_analyzer.get_age(target)
        if target_age == -1:
            target_age = "не указан"
        friends_ages = age_analyzer.get_friends_ages(target)
        predicted = (neural_network.query(friends_ages))
        mode = find_max_mode(friends_ages)
        response = f"Мы проанализировали {target_name['first_name']} {target_name['last_name']}\n" \
                   f"Возраст, указанный в профиле - {target_age}.\n" \
                   f"Однако, мы полагаем, что настоящий возраст: {predicted} \n" \
                   f"Мода: {mode}"

        bot.send_message(message.chat.id, response)
        logging.info(f"analyze_response^Answered to {by}. Request: {message.chat.id}")


@bot.message_handler(commands=["histogram"])
def build_histogram(message):
    by = f"{message.chat.first_name} {message.chat.last_name} ({message.chat.id})"
    try:
        target = (message.text.split(' '))[1]
    except:
        logging.info(f"histogram_response^Wrong format. Requested by {by}")
        bot.send_message(message.chat.id, "Введите по формату\n"
                                          "/histogram {id}")
        return
    logging.info(f"histogram_request^{by} wants to build histogram {target}")
    ages = age_analyzer.get_friends_ages(target)
    if age_analyzer.is_profile_closed(target) or ages == "PC":
        logging.info(f"histogram_response^{target} - no profile. Requested by {by}")
        bot.send_message(message.chat.id, "Страница закрыта или не существует. Попробуйте еще раз.")
    else:
        bot.send_message(message.chat.id, f"Мы начали анализировать {target}")
        logging.info(f"histogram_start^Started analyze {target} to build histogram. Requested by {by}")
        target_name = age_analyzer.get_name(target)
        ages = age_analyzer.get_friends_ages(target=target)
        y = counts_by_arr(ages)
        x = range(len(y))
        plt.figure(figsize=(15, 5), dpi=80)
        plt.bar(x=x, height=y)
        plt.xlim(min(ages) - 5, max(ages) + 5)
        plt.ylim(0, max(y) + 5)
        plt.yticks(np.arange(0, max(y) + 5, 5))
        plt.xticks(np.arange(min(ages) - (int(min(ages)) % 5), max(ages) + 5, 5))
        plt.title(f"{target_name['first_name']} {target_name['last_name']}", fontsize=24)
        plt.ylabel("Count", fontsize=16)
        plt.xlabel("Age", fontsize=16)
        plt.savefig(f"{settings.project_folder}/graph/{target}.png")
        logging.info(
            f"histogram_response^Histogram saved to {settings.project_folder}/graph/{target}.png. Sending it back.")
        photo = open(f"{settings.project_folder}/graph/{target}.png", 'rb')
        bot.send_message(message.chat.id,
                         f"Мы построили гистограмму возрастов друзей"
                         f" пользователя {target_name['first_name']} {target_name['last_name']}.")
        bot.send_chat_action(message.chat.id, 'upload_photo')
        bot.send_photo(message.chat.id, photo)
        plt.close()
        photo.close()
