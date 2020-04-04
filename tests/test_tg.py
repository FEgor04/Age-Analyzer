import pytest

import neuroanalyzer
import tg as telegram_bot


class Chat:
    def __init__(self, f_name, l_name, _id):
        self.first_name = f_name
        self.last_name = l_name
        self.id = _id


class Message:
    def __init__(self, f_name, l_name, id_, text):
        self.chat = Chat(f_name, l_name, id_)
        self.text = text


test_data = [
    Message("It's", "fine", 1, "/analyze fegor2004"),
    Message("It's", "fine too", 1, "/analyze lesese"),
    Message("No", "Page", 2, "/analyze asdasgfgaasdasd"),
    Message("Wrong", "Format", 3, "/analyze")
]


@pytest.mark.parametrize("message", test_data)
def test_analyze(message):
    model = neuroanalyzer.AgeRegressor()
    model.open_model('neuronet.sav')
    assert telegram_bot.analyze(message, True, model) == message.chat.id


@pytest.mark.parametrize("message", test_data)
def test_build_histogram(message):
    assert telegram_bot.build_histogram(message, True) == message.chat.id


@pytest.mark.parametrize("message", test_data)
def test_analyze_recursive(message):
    model = neuroanalyzer.AgeRegressor()
    model.open_model('neuronet.sav')
    assert telegram_bot.analyze_recursive(message, True, model) == message.chat.id
