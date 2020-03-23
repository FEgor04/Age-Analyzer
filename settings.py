import os
from typing import Tuple

version = 5.103
folder = 'csv/'
csv_file = 'age_research1.csv'
analyze = True
log_needed = True
project_folder = "."
tg_api = os.environ.get('tg_api')
token = os.environ.get('vk_api')
neural_network_file = 'neuronet.sav'
min_version: Tuple[int, int, int] = (3, 6, 10)  # Version in which statistics._counts is present (NEEDED FOR TESTS)
