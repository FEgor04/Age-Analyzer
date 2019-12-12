
import csv_connect as csv
import age_analyzer as analyzer
import matplotlib.pylab as plt
from settings import input_file, output_file, analyze_input_file, regression_data
import settings
import numpy as np

if __name__ == "__main__":
    if settings.analyze:
        # csv.fill_vk_age(input_file, output_file)
        # csv.fill_friends_age(output_file, output_file)
        csv.analyze(analyze_input_file)
        # csv.prepare_regression_dataset(analyze_input_file, regression_data)
    else:
        settings.target = (input())
        print(analyzer.get_friends_ages(settings.target))
        print(round(analyzer.get_age_with_equation(settings.target), 0))
    # target = "fegor2004"
    # histo = analyzer.build_friends_age_hist(target)
    # plt.grid(1)
    # plt.xlim(0, 60)
    # # plt.ylim(0, 50)
    # plt.title(target)
    # plt.ylabel("Count")
    # plt.xlabel("Age")
    # plt.show()
    #
