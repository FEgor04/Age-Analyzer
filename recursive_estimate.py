from multiprocessing.pool import ThreadPool

import age_analyzer
from neuroanalyzer import AgeRegressor


def recursive_function(friends: list, count: int, number: int, model: AgeRegressor, target_id: str):
    """

    :param friends: List with target's friends
    :param count: How many threads in all
    :param number: What is the number of this thread (From 0)
    :param model: AgeRegressor model
    :param target_id: target's id
    :return:
    """
    ln = len(friends)
    friends_part = friends[int((ln / count) * number): int((ln / count) * (number + 1))]
    estimated_ages = []
    for person in friends_part:
        if person != target_id:
            estimated_age = model.query(person)
            if estimated_age != -1:
                estimated_ages.append(estimated_age)
    return estimated_ages


def estimate_age_recursive(target, model: AgeRegressor, threads_cnt=3) -> float:
    """Estimate target's age with recursive algorithm.
    :param threads_cnt: How many threads will you run
    :param target: Whom to analyze
    :param model: AgeRegressor model
    :return: Estimated age
    """
    target_friends = age_analyzer.get_friends(target)
    target_id = age_analyzer.get_id_by_domain(target)
    estimated_ages = []
    threads = []
    if isinstance(target_friends, int):
        return -1  # Profile closed
    pool = ThreadPool(processes=threads_cnt)
    for i in range(threads_cnt):
        async_result = pool.apply_async(recursive_function, (target_friends, threads_cnt, i, model, target_id))
        threads.append(async_result)
    for i in range(threads_cnt):
        return_val = threads[i].get()
        estimated_ages.extend(return_val)
    return model._query(estimated_ages)
