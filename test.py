import settings
import age_analyzer
import neuroanalyzer
import pytest


def test_get_age():
    """
    Test age_analyzer.get_age function
    """
    age = age_analyzer.get_age("fegor2004")
    assert age == 24


def test_get_bdate():
    """
    Test age_analyzer.get_bdate function
    """
    bdate = age_analyzer.get_bdate("fegor2004")
    assert bdate == '5.8.1995'


def test_get_friends_bdates():
    """
    Test age_analyzer.get_freinds_bdates function
    """
    bdates = age_analyzer.get_friends_bdate("fegor2004")
    assert bdates != "PC"


def test_get_friends_ages():
    """
    Test age_analyzer.get_friends_ages function
    """
    ages = age_analyzer.get_friends_ages("fegor2004")
    assert ages != "PC"


def test_get_age_by_bdate():
    """
    Test age_analyzer.get_age_by_bdate function
    """
    age = age_analyzer.get_age_by_bdate('5.8.2004')
    assert age == 15


def test_get_id_by_domain():
    """
    Test age_analyzer.get_id_by_domain function
    """
    id = age_analyzer.get_id_by_domain("fegor2004")
    assert id == 251024930


def test_open_model():
    """
    Test neoruanalyzer.open_model function
    """
    reg = neuroanalyzer.NeuralNetwork
    reg.open_model(reg, filename=settings.project_folder + '/' + settings.neural_network_file)
    assert 1 == 1  # It test if there will be no exception, so it is okay


def test_save_model():
    """
    Test neoruanalyzer.save_model function
    """
    reg = neuroanalyzer.NeuralNetwork
    reg.open_model(reg, filename=settings.project_folder + '/' + settings.neural_network_file)
    reg.save_model(reg, filename=settings.project_folder + '/' + settings.neural_network_file)
    assert 1 == 1  # It test if there will be no exception, so it is okay


def test_query():
    """
    Test neoruanalyzer.query function
    """
    reg = neuroanalyzer.NeuralNetwork
    reg.open_model(reg, filename=settings.project_folder + '/' + settings.neural_network_file)
    predicted = reg.query(reg,
                          [21, 21, 21, 24, 24, 51, 51, 24, 17, 16, 16, 22, 91, 91, 91, 21, 15, 15, 25, 15, 14, 35, 34,
                           20, 20, 28, 15, 16, 20, 15, 24, 47, 25, 15, 16])
    assert 15 == pytest.approx(predicted, 5)
