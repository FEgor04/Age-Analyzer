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


@pytest.mark.parametrize("target, expected, deviation",
                         [
                             ("fegor2004", 15, 1),
                             ("asdasdassfjsdsfsfjsdzdfjgdd", -1, 0)  # No profile
                         ])
def test_estimate_age_recursive(target, expected, deviation):
    """Test tg.estimate_age_recursive function
    :param target: Target, whom to analyze
    :param expected: expected answer
    :param deviation: Allowed deviation |expected-answer| <= deviation
    :return: Asserts True if it was correct
    """
    model = neuroanalyzer.AgeRegressor()
    model.open_model('neuronet.sav')
    estimated_age = telegram_bot.estimate_age_recursive(target, model)
    if expected == -1:
        assert estimated_age == expected
    assert abs(estimated_age - expected) <= deviation


@pytest.mark.parametrize("message", [
    Message("It's", "fine", 1, "/analyze fegor2004"),
    Message("No", "Page", 2, "/analyze asdasgfgaasdasd"),
    Message("Wrong", "Format", 3, "/analyze")
])
def test_analyze(message):
    model = neuroanalyzer.AgeRegressor()
    model.open_model('neuronet.sav')
    print(message.chat.id)
    assert telegram_bot.analyze(message, launched_by_test=True, model=model) == message.chat.id


@pytest.mark.parametrize("message", [
    Message("It's", "fine", 1, "/analyze fegor2004"),
    Message("No", "Page", 2, "/analyze asdasgfgaasdasd"),
    Message("Wrong", "Format", 3, "/analyze")
])
def test_build_histogram(message):
    assert True


@pytest.mark.parametrize("message", [
    Message("It's", "fine", 1, "/analyze fegor2004"),
    Message("No", "Page", 2, "/analyze asdasgfgaasdasd"),
    Message("Wrong", "Format", 3, "/analyze")
])
def test_analyze_recursive(message):
    assert True
