import settings
import age_analyzer
import neuroanalyzer
import pytest
from unittest.mock import Mock


@pytest.mark.parametrize("target, expected", [
    ('fegor2004', 24),
    ('gallium', 20)
])
def test_get_age(target: str, expected: int):
    """
    Test age_analyzer.get_age function
    """
    age = age_analyzer.get_age(target)
    assert age == expected, f"Should be {expected}"


@pytest.mark.parametrize("target, expected", [
    ('fegor2004', '5.8.1995'),
    ('gallium', '9.7.1999')
])
def test_get_bdate(target: str, expected: str):
    """
    Test age_analyzer.get_bdate function
    """
    bdate = age_analyzer.get_bdate(target)
    assert bdate == expected, f"Should be {expected}"


@pytest.mark.parametrize("target, wrong, comment", [
    ("fegor2004", "PC", "Profile is open, so it should not give PC"),
    ("dasdasdaatggrtefsdg", [], "There is no profile")
])
def test_get_friends_bdates(target: str, wrong, comment):
    """
    Test age_analyzer.get_freinds_bdates function
    """
    bdates = age_analyzer.get_friends_bdate(target)
    assert bdates != wrong, comment


@pytest.mark.parametrize("target, wrong, comment", [
    ('fegor2004', 'PC', "Profile is open, so it should not give PC"),
    ("dasdasdaatggrtefsdg", [], "There is no profile")
])
def test_get_friends_ages(target: str, wrong, comment):  # It shouldn't give wrong answer
    """
    Test age_analyzer.get_friends_ages function
    """
    ages = age_analyzer.get_friends_ages(target)
    assert ages != wrong, comment


@pytest.mark.parametrize("bdate, expected", [
    ('5.8.2004', 15),
    ('2.2.2000', 20),
    ('3.3.2000', 20),
    ('12.12.2000', 19),
    ('3.3.2020', 0),
    ('5.5', -1),
    (-1, -1)
])
def test_get_age_by_bdate(bdate: str, expected: int):
    """
    Test age_analyzer.get_age_by_bdate function
    """
    age = age_analyzer.get_age_by_bdate(bdate)
    assert age == expected, f"Should be {expected}"


@pytest.mark.parametrize("target, expected", [
    ("fegor2004", 251024930),
    ("azlexa", 225757601)
])
def test_get_id_by_domain(target: str, expected: int):
    """
    Test age_analyzer.get_id_by_domain function
    """
    id = age_analyzer.get_id_by_domain(target)
    assert id == expected, f"Should be {expected}"


@pytest.mark.parametrize("array, expected", [
    ([1, 2, 2, 2, 3], 2),
    ([1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4], 3)
])
def test_find_average_mode(array: list, expected: int):
    """
    Test age_analyzer.find_average_mode function
    :return:
    """
    assert expected == age_analyzer.find_average_mode(array), f"Should be {expected}"


@pytest.mark.parametrize("array, expected", [
    ([1, 2, 2, 2, 3, 3, 3, 3], 3),  # Test when there is only one mode
    ([1, 2, 2, 2, 3, 3, 3, 4, 4], 3),  # Test when there is many modes
    ([1], 1)  # Test when there is only one elem
])
def test_find_max_mode(array: list, expected: int):
    """
    Test age_analyzer.find_average_mode function
    :return:
    """
    assert expected == age_analyzer.find_max_mode(array), f"Should be {expected}"


@pytest.mark.parametrize("target, expected", [
    ('fegor2004', False),
    ('id41417392', True),
    ('sasassaasdas', True)  # There is no profile like that
])
def test_is_profile_closed(target: str, expected: bool):
    """
    Test age_analyzer.is_profile_closed function
    """
    pred = age_analyzer.is_profile_closed(target)
    assert expected == pred


@pytest.mark.parametrize("target, expected", [
    ("fegor2004", -1),
])
def test_get_friends(target, expected):
    """
    Test age_analyzer.get_friends function
    """
    friends = age_analyzer.get_friends(target)
    assert expected == pytest.approx(len(friends), 3)


@pytest.mark.parametrize("target, expected", [
    ("fegor2004", "Egor Fedorov"),
    ("ms6mtudgpymryvn9rfz4cwlpjdrqvwpn", "Nikita Lazarev")
])
def test_get_name(target, expected):
    """
    Test age_analyzer.get_name function
    """
    name = age_analyzer.get_name(target)
    assert name['first_name'] + ' ' + name['last_name'] == expected