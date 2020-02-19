import unittest
import settings
import age_analyzer
import neuroanalyzer

class VkScrapperTest(unittest.TestCase):
    def test_get_age(self):
        age = age_analyzer.get_age("fegor2004")
        self.assertEqual(age, 24)

    def test_get_bdate(self):
        bdate = age_analyzer.get_bdate("fegor2004")
        self.assertEqual(bdate, '5.8.1995')

    def test_get_friends_bdates(self):
        bdates = age_analyzer.get_friends_bdate("fegor2004")
        self.assertNotEqual(bdates, "PC")

    def test_get_friends_ages(self):
        ages = age_analyzer.get_friends_ages("fegor2004")
        self.assertNotEqual(ages, "PC")

    def test_get_age_by_bdate(self):
        age = age_analyzer.get_age_by_bdate('5.8.2004')
        self.assertEqual(age, 15)

    def test_get_id_by_domain(self):
        id = age_analyzer.get_id_by_domain("fegor2004")
        self.assertEqual(id, 251024930)

class NeuralNetworkTest(unittest.TestCase):
    def test_open_model(self):
        reg = neuroanalyzer.NeuralNetwork
        reg.open_model(reg, settings.project_folder + '/' + settings.neural_network_file)
        self.assertTrue(True)

    def test_save_model(self):
        reg = neuroanalyzer.NeuralNetwork
        reg.open_model(reg, settings.project_folder + '/' + settings.neural_network_file)
        reg.save_model(reg, settings.project_folder + '/' + settings.neural_network_file)
        self.assertTrue(True)

    def test_query(self):
        reg = neuroanalyzer.NeuralNetwork
        reg.open_model(reg, settings.project_folder + '/' + settings.neural_network_file)
        predicted = reg.query(reg, [21, 21, 21, 24, 24, 51, 51, 24, 17, 16, 16, 22, 91, 91, 91, 21, 15, 15, 25, 15, 14, 35, 34, 20, 20, 28, 15, 16, 20, 15, 24, 47, 25, 15, 16])
        self.assertAlmostEqual(predicted, 15, delta=5)

if __name__ == '__main__':
    unittest.main()
