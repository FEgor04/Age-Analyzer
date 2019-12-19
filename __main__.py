
import csv_connect as csv
import age_analyzer as analyzer
import matplotlib.pylab as plt
from settings import input_file, output_file, analyze_input_file
import settings
import neuroanalyzer
import telebot
# import tg
import numpy as np

if __name__ == "__main__":
    # print(analyzer.get_friends_ages("fegor2004"))
    # tg.bot.polling()
    # if settings.analyze:
    csv.fill_vk_age(input_file, output_file)
    csv.fill_friends_age(output_file, output_file)
        # csv.analyze(analyze_input_file)
        # csv.prepare_regression_dataset(analyze_input_file, regression_data)
        # pass
    # else:
    #     settings.target = (input())
    #     print(analyzer.get_friends_ages(settings.target))
    #     print(round(analyzer.get_age_with_equation(settings.target), 0))
    # target = "fegor2004"
    # histo = analyzer.build_friends_age_hist(target)
    # plt.grid(1)
    # plt.xlim(0, 60)
    # # plt.ylim(0, 50)
    # plt.title(target)
    # plt.ylabel("Count")
    # plt.xlabel("Age")
    # plt.show()
    # neuro = neuroanalyzer.neuralNetwork()
    # neuro.train('csv/neur')
    #
[21, 21, 24, 24, 51, 51, 24, 16, 16, 16, 15, 15, 15, 21, 15, 15, 22, 25, 15, 14, 16, 34, 19, 19, 28, 15, 20, 15, 24, 25, 15, 15, 15, 16]
[21, 21, 24, 24, 51, 51, 24, 16, 16, 16, 21, 22, 25, 16, 34, 19, 19, 28, 20, 24, 25, 16]
