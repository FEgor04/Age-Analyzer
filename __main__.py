import csv_connect as csv
import age_analyzer as analyzer
from settings import input_file, output_file, analyze_file
import settigs

if __name__ == "__main__":
    if settigs.analyze:
        csv.analyze(analyze_file)
    else:
        analyzer.get_friends_ages(settigs.target)
