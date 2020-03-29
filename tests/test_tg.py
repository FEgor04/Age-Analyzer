import pytest

import neuroanalyzer
import tg as telegram_bot


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
