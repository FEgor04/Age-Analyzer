import pytest

import neuroanalyzer


@pytest.mark.parametrize("target, expected, deviation, threads",
                         [
                             ("asdasdassfjsdsfsfjsdzdfjgdd", -1, 0, 1),  # No profile
                             ("asdasdassfjsdsfsfjsdzdfjgdd", -1, 0, 2),  # No profile
                             ("asdasdassfjsdsfsfjsdzdfjgdd", -1, 0, 3),  # No profile
                             ("asdasdassfjsdsfsfjsdzdfjgdd", -1, 0, 4),  # No profile
                             # ("fegor2004", 15, 1, 1),
                             # ("fegor2004", 15, 1, 2),
                             ("fegor2004", 15, 1, 3),
                             # ("fegor2004", 15, 1, 4)
                         ])
def test_estimate_age_recursive(target: str, expected: float, deviation: float, threads: int):
    """Test tg.estimate_age_recursive function
    :param target: Target, whom to analyze
    :param expected: expected answer
    :param deviation: Allowed deviation |expected-answer| <= deviation
    :return: Asserts True if it was correct
    """
    model = neuroanalyzer.AgeRegressor()
    model.open_model('neuronet.sav')
    estimated_age = recursive_estimate.estimate_age_recursive(target, model, threads)
    if expected == -1:
        assert estimated_age == expected
    assert abs(estimated_age - expected) <= deviation


import recursive_estimate
