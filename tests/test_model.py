import neuroanalyzer
import settings


def test_init():
    reg = neuroanalyzer.AgeRegressor()
    reg.__init__()
    assert 1 == 1, "It should not give any exceptions"


def test_open_model():
    """
    Test neoruanalyzer.open_model function
    """
    reg = neuroanalyzer.AgeRegressor()
    reg.open_model(settings.project_folder + '/' + settings.neural_network_file)
    assert 1 == 1, "It should not give any exceptions"  # Passed if there will be no exception, so it is okay


def test_save_model():
    """
    Test neoruanalyzer.save_model function
    """
    reg = neuroanalyzer.AgeRegressor()
    reg.open_model(settings.project_folder + '/' + settings.neural_network_file)
    reg.save_model(settings.project_folder + '/' + settings.neural_network_file)
    assert 1 == 1, "It should not give any exceptions"  # Passed if there will be no exception, so it is okay


def test_query():
    """
    Test neoruanalyzer.query function
    """
    reg = neuroanalyzer.AgeRegressor()
    reg.open_model(settings.project_folder + '/' + settings.neural_network_file)
    predicted = reg._query(
        [21, 21, 21, 24, 24, 51, 51, 24, 17, 16, 16, 22, 91, 91, 91, 21, 15, 15, 25, 15, 14, 35, 34,
         20, 20, 28, 15, 16, 20, 15, 24, 47, 25, 15, 16])
    assert abs(15 - predicted) <= 1, "Should be 15±1"


def test_train_with_raw_data():
    """
    Test neuroanalyzer.train_with_raw_data() function
    :return:
    """
    reg = neuroanalyzer.AgeRegressor()
    reg.train_with_raw_data([], True)
    # Passed if there will be no exception, so it is okay
    assert 1 == 1, "It should not give any exceptions"
