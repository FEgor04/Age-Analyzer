import age_analyzer
import neuroanalyzer
import settings
import tg as telegram_bot

if __name__ == "__main__":
    if settings.analyze:
        print("Input target's ID", end=": ")
        target = input()
        neural_network = neuroanalyzer.NeuralNetwork
        neural_network.open_model(self=neural_network, filename=settings.neural_network_file)
        ages = age_analyzer.get_friends_ages(target=target)
        name = age_analyzer.get_name(target=target)
        try:
            predicted = neural_network.query(self=neural_network, ages=ages)
            answer = f"Neural network thinks that {name['first_name']} {name['last_name']} ({target}) age is {predicted}"
        except:
            answer = "Profile closed"
        print(answer)
        pass
    else:
        telegram_bot.launch()
