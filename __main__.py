import csv_connect as csv
import age_analyzer as analyzer
from settings import input_file, output_file, analyze_input_file, regression_data
import settings

if __name__ == "__main__":
    if settings.analyze:
        # csv.fill_vk_age(input_file, output_file)
        # csv.fill_friends_age(output_file, output_file)
        csv.analyze(analyze_input_file)
        # csv.prepare_regression_dataset(analyze_input_file, regression_data)
    else:
        analyzer.get_friends_ages(settings.target)
