from threading import Thread

import age_analyzer
from neuroanalyzer import AgeRegressor


class RecursiveThread(Thread):
    """
    Thread class for Recursive Analyze
    """

    def __init__(self, friends, count, number, model, target_id):
        """
        Initialization
        :param friends: all friends
        :param count: how many parts
        :param number: what is the number of this thread (From zero)
        """
        Thread.__init__(self)
        ln = len(friends)
        self.friends = friends[int((ln / count) * number): int((ln / count) * (number + 1))]
        self.model = model
        self._return_value = []
        self.target_id = target_id

    def run(self):
        estimated_ages = []
        for person in self.friends:
            person_ages = age_analyzer.get_friends_ages(person)
            if isinstance(person_ages, list) and person != self.target_id and len(person_ages) != 0:
                estimated_ages.append(self.model.query(person_ages, False, False))
        self._return_value = estimated_ages

    def join(self):
        return self._return_value


def estimate_age_recursive(target, model: AgeRegressor, threads=1) -> float:
    """Estimate target's age with recursive algorithm.
    :param threads: How many threads will you run
    :param target: Whom to analyze
    :param model: AgeRegressor model
    :return: Estimated age
    """
    target_friends = age_analyzer.get_friends(target)
    target_id = age_analyzer.get_id_by_domain(target)
    estimated_ages = []
    # print(target_friends)
    if isinstance(target_friends, int):
        return -1  # Profile closed
    for i in range(threads):
        my_thread = RecursiveThread(target_friends, threads, i, model, target_id)
        my_thread.start()
        my_thread.run()
        estimated_ages.extend(my_thread.join())
    return model.query(estimated_ages)
