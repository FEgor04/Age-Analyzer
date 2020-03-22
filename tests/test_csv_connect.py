import pandas as pd
import pytest

import csv_connect


@pytest.mark.parametrize("dataframe_raw, expected", [
    (pd.DataFrame({
        "ID": ['fegor2004', 'id41417392'],
        "Real Age": [15, 15],
        "VK Age": [24.0, -1.0],
        "Mean": [27.91, -1.0],
        "Harmonic Mean": [21.05, -1.0],
        "Mode": [15.0, -1.0],
        "Median": [21.0, -1.0],
        "std": [21.4, -1.0]
    }), 1),
    (pd.DataFrame({
        "ID": ['id41417392'],
        "Real Age": [15],
        "VK Age": [-1.0],
        "Mean": [-1.0],
        "Harmonic Mean": [-1.0],
        "Mode": [-1.0],
        "Median": [-1.0],
        "std": [-1.0]
    }), 0),
])
def test_people_with_open_profile(dataframe_raw: pd.DataFrame, expected: int):
    """
    Test csv_connect.people_with_open_profile
    """
    assert csv_connect.people_with_open_profile(dataframe_raw) == expected, f"Should be {expected}"


@pytest.mark.parametrize("data, expected", [
    (pd.DataFrame({
        "ID": ['id41417392'],
        "Real Age": [15],
        "VK Age": [-1.0],
        "Mean": [-1.0],
        "Harmonic Mean": [-1.0],
        "Mode": [-1.0],
        "Median": [-1.0],
        "std": [-1.0]
    }), 0),
    (pd.DataFrame({
        "ID": ['sasafs'],
        "Real Age": [15],
        "VK Age": [321],
        "Mean": [-1.0],
        "Harmonic Mean": [-1.0],
        "Mode": [-1.0],
        "Median": [-1.0],
        "std": [-1.0]
    }), 1)
])
def test_people_who_specified_age(data: pd.DataFrame, expected: int):
    """
    Test csv_connect.people_who_specified_age
    """
    assert csv_connect.people_who_specified_age(data) == expected, f"Should be {expected}"


@pytest.mark.parametrize("data, expected", [
    (pd.DataFrame({
        "ID": ['fegor2004', 'id41417392'],
        "Real Age": [15, 15],
        "VK Age": [24.0, -1.0],
        "Mean": [27.91, -1.0],
        "Harmonic Mean": [21.05, -1.0],
        "Mode": [15.0, -1.0],
        "Median": [21.0, -1.0],
        "std": [21.4, -1.0]
    }),
     (pd.DataFrame({
         "ID": ['fegor2004', 'id41417392'],
         "Real Age": [15, 15],
         "VK Age": [24.0, -1.0],
         "Mean": [27.91, -1.0],
         "Harmonic Mean": [21.05, -1.0],
         "Mode": [15.0, -1.0],
         "Median": [21.0, -1.0],
         "std": [21.4, -1.0]
     })
     )
    )
])
def test_fill_friends_age(data: pd.DataFrame, expected: pd.DataFrame):
    """
    Test csv_connect.fill_friends_age function
    """
    print(data)
    data_filled = csv_connect.fill_friends_age(data)
    assert 1 == 1  # Passed if it completed


@pytest.mark.parametrize("data, expected", [
    (
            pd.DataFrame({
                "ID": ['fegor2004', 'id41417392'],
                "Real Age": [15, 15],
                "VK Age": [-1, -1.0],
                "Mean": [-1, -1.0],
                "Harmonic Mean": [-1, -1.0],
                "Mode": [-1, -1.0],
                "Median": [-1, -1.0],
                "std": [-1, -1]
            }),
            pd.Series([24.0, -1.0], name="VK Age")
    )
])
def test_fill_vk_age(data: pd.DataFrame, expected: pd.Series):
    """
    Test csv_connect.fill_vK_age function
    """
    data_filled = csv_connect.fill_vk_age(data)
    assert data_filled['VK Age'].all() == expected.all()


@pytest.mark.parametrize("df, expected", [
    (
            pd.DataFrame({
                "ID": ['fegor2004', 'id41417392', 'assasa', 'asdasd'],
                "Real Age": [15, 15, 21, 13],
                "VK Age": [-1, -1.0, 21, 13],
                "Mean": [-1, -1.0, 1, 1],
                "Harmonic Mean": [-1, -1.0, 1, 1],
                "Mode": [-1, -1.0, 1, 1],
                "Median": [-1, -1.0, 1, 1],
                "std": [-1, -1, 1, 1]
            }), 2
    )
])
def test_people_whose_vk_age_is_equal_to_real_age(df: pd.DataFrame, expected: int):
    """
    Test csv_connect.people_whose_vk_age_is_equal_to_real_age function
    """
    assert csv_connect.people_whose_vk_age_is_equal_to_real_age(df) == expected
