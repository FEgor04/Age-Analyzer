import datetime
import statistics as st

import matplotlib.pyplot as plt
import telebot

import age_analyzer
import neuroanalyzer
import settings
from neuroanalyzer import NeuralNetwork

bot = telebot.TeleBot(settings.tg_api)
neural_network: NeuralNetwork = neuroanalyzer.NeuralNetwork()


def launch() -> object:
    try:
        neural_network.open_model(settings.neural_network_file)
    except:
        neural_network.train('csv/age_research_filled.csv')
    bot.polling()


def log(event, text, file):
    read = open(file, 'r')
    file_text = read.read()
    read.close()
    now = datetime.datetime.now()
    log_text = f"{now}::{event}::{text}"
    f = open(file, 'w')
    f.write(file_text + log_text + '\n')


def find_max_mode(list1):
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
        to_build = "ddd"
    log("REQUEST", f"{by} wants to analyze {to_build}", "log/telegram.log")
    ages = age_analyzer.get_friends_ages(to_build)
    if age_analyzer.is_profile_closed(to_build) or ages == "PC":
        log("RESPONSE", f"{message.chat.id} - no profile. Requested by {by}", "log/telegram.log")
        bot.send_message(message.chat.id, "Страница закрыта или не существует. Попробуйте еще раз.")
    else:
        bot.send_message(message.chat.id, f"Мы начали анализировать {to_build}")
        log("ANALYZING", f"Started analyze {to_build}. Requested by {by}", "log/telegram.log")
        target_name = age_analyzer.get_name(to_build)
        target_age = age_analyzer.get_age(to_build)
        if target_age == -1:
            target_age = "не указан"
        friends_ages = age_analyzer.get_friends_ages(to_build)
        print(f"ID: {to_build}. Ages: {friends_ages}")
        predicted = neural_network.query(friends_ages)

        response = f"Мы проанализировали {target_name['first_name']} {target_name['last_name']}\n" \
                   f"Возраст, указанный в профиле - {target_age}.\n" \
                   f"Однако, мы полагаем, что настоящий возраст - {predicted} "

        bot.send_message(message.chat.id, response)
        log("RESPONSE", f"Answered to {by}. Request: {message.chat.id}", "log/telegram.log")


@bot.message_handler(commands=["histogram"])
def build_histogram(message):
    by = f"{message.chat.first_name} {message.chat.last_name} ({message.chat.id})"
    to_build = (message.text.split(' '))[1]
    log("REQUEST", f"{by} wants to build graph {message.text}", "log/telegram.log")
    ages = age_analyzer.get_friends_ages(to_build)
    if age_analyzer.is_profile_closed(to_build) or ages == "PC":
        log("RESPONSE", f"{message.chat.id} - no profile. Requested by {by}", "log/telegram.log")
        bot.send_message(message.chat.id, "Страница закрыта или не существует. Попробуйте еще раз.")
    else:
        bot.send_message(message.chat.id, f"Мы начали анализировать {to_build}")
        log("GRAPH", f"Started analyze {to_build} to build graph. Requested by {by}", "log/telegram.log")
        target_name = age_analyzer.get_name(to_build)
        # target_age = age_analyzer.get_age(to_build)
        ages = age_analyzer.get_friends_ages(target=to_build)

        hist = plt.hist(ages)
        plt.grid(1)
        plt.xlim(0, 60)
        plt.title(f"{target_name['first_name']} {target_name['last_name']}")
        plt.ylabel("Count")
        plt.xlabel("Age")
        plt.savefig(f"graph/{to_build}.png")
        photo = open(f"graph/{to_build}.png", 'rb')
        bot.send_message(message.chat.id,
                         f"Мы построили гистограмму возрастов друзей"
                         f" пользователя {target_name['first_name']} {target_name['last_name']}.")
        bot.send_chat_action(message.chat.id, 'upload_photo')
        bot.send_photo(message.chat.id, photo)
        plt.close()
        photo.close()

