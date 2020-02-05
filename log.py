import settings
import datetime


def log(event: str, text: str, file: str, folder=settings.project_folder):
    """

    :param event: what happened
    :param text: description
    :param file: where to log
    :param folder: folder to save
    :return Makes log formatted like this: TIME::EVENT::TEXT. It will put it in file
    """
    if settings.log_needed:
        read = open(folder + '/' + file, 'r')
        file_text = read.read()
        read.close()
        now = datetime.datetime.now()
        log_text = f"{now}::{event}::{text}"
        f = open(folder + '/' + file, 'w')
        f.write(file_text + log_text + '\n')
    else:
        pass