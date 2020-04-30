import datetime
import statistics as st

import pandas as pd
import psycopg2

import age_analyzer
import neuroanalyzer
import settings


def create_table():
    connection = psycopg2.connect(
        database=settings.db_name,
        user=settings.db_login,
        password=settings.db_pass,
        host=settings.db_ip,
        port=settings.db_port
    )
    cur = connection.cursor()
    cur.execute(' \
        CREATE TABLE IF NOT EXISTS analyzed( \
        id integer not null unique, \
        domain varchar(250), \
        first_name varchar(250), \
        last_name varchar(250), \
        estimated_age real, \
        real_age real, \
        mean real, \
        mode real, \
        harmonic_mean real, \
        median real, \
        std real, \
        friends_cnt integer, \
        verified bool, \
        last_check date, \
        vk_age integer \
    )')
    connection.commit()
    connection.close()


def upgrade(domain, model):
    target_id = age_analyzer.get_id_by_domain(domain)
    domain = age_analyzer.get_domain_by_id(target_id)
    connection = psycopg2.connect(
        database=settings.db_name,
        user=settings.db_login,
        password=settings.db_pass,
        host=settings.db_ip,
        port=settings.db_port
    )
    cur = connection.cursor()
    ages = age_analyzer.get_friends_ages(target_id)
    estimated_age = model._query(ages)
    name = age_analyzer.get_name(target_id)
    mean = round(st.mean(ages), 2)
    hmean = round(st.harmonic_mean(ages), 2)
    mode = round(neuroanalyzer.find_average_mode(ages), 2)
    median = round(st.median(ages), 2)
    std = round(neuroanalyzer.find_std(ages), 2)
    vk_age = age_analyzer.get_age(target_id)
    friends_cnt = len(ages)
    query = (f"UPDATE analyzed SET estimated_age = {estimated_age} WHERE id=\'{target_id}\';"
             f"UPDATE analyzed SET mean = {mean} WHERE id=\'{target_id}\';"
             f"UPDATE analyzed SET harmonic_mean = {hmean} WHERE id=\'{target_id}\';"
             f"UPDATE analyzed SET mode = {mode} WHERE id=\'{target_id}\';"
             f"UPDATE analyzed SET median = {median} WHERE id=\'{target_id}\';"
             f"UPDATE analyzed SET std = {std} WHERE id=\'{target_id}\';"
             f"UPDATE analyzed SET last_check = current_date WHERE id=\'{target_id}\';"
             f"UPDATE analyzed SET friends_cnt = {friends_cnt} WHERE id=\'{target_id}\';"
             f"UPDATE analyzed SET first_name = \'{name['first_name']}\' WHERE id=\'{target_id}\';"
             f"UPDATE analyzed SET last_name = \'{name['last_name']}\' WHERE id=\'{target_id}\';"
             f"UPDATE analyzed SET domain = \'{domain}\' WHERE id = \'{target_id}\'"
             )
    cur.execute(query)
    connection.commit()
    connection.close()
    return estimated_age


def check_was_analyzed_recently(domain):
    target_id = age_analyzer.get_id_by_domain(domain)
    domain = age_analyzer.get_domain_by_id(target_id)
    if not target_id:
        return 0
    connection = psycopg2.connect(
        database=settings.db_name,
        user=settings.db_login,
        password=settings.db_pass,
        host=settings.db_ip,
        port=settings.db_port
    )
    cur = connection.cursor()
    cur.execute(
        f"SELECT count(*) FROM analyzed WHERE id=\'{target_id}\' AND abs(last_check-current_date)<=1")
    records = cur.fetchall()
    connection.commit()
    connection.close()
    return records[0][0]


def check_was_analyzed_ever(domain):
    target_id = age_analyzer.get_id_by_domain(domain)
    domain = age_analyzer.get_domain_by_id(target_id)
    if not target_id:
        return 0
    connection = psycopg2.connect(
        database=settings.db_name,
        user=settings.db_login,
        password=settings.db_pass,
        host=settings.db_ip,
        port=settings.db_port
    )
    cur = connection.cursor()
    cur.execute(
        f"SELECT count(*) FROM analyzed WHERE id=\'{target_id}\'")
    records = cur.fetchall()
    connection.commit()
    connection.close()
    return records[0][0]


def get_age_from_database(domain):
    target_id = age_analyzer.get_id_by_domain(domain)
    domain = age_analyzer.get_domain_by_id(target_id)
    connection = psycopg2.connect(
        database=settings.db_name,
        user=settings.db_login,
        password=settings.db_pass,
        host=settings.db_ip,
        port=settings.db_port
    )
    cur = connection.cursor()
    cur.execute(f"SELECT estimated_age FROM analyzed WHERE id=\'{target_id}\' and abs(last_check-current_date)<=1")
    records = cur.fetchall()
    connection.commit()
    connection.close()
    if not records:
        return 0
    else:
        return records[0][0]


def analyze_and_insert(target, model, force_upgrade=False):
    connection = psycopg2.connect(
        database=settings.db_name,
        user=settings.db_login,
        password=settings.db_pass,
        host=settings.db_ip,
        port=settings.db_port
    )
    target_id = age_analyzer.get_id_by_domain(target)
    domain = age_analyzer.get_domain_by_id(target_id)
    was_analyzed_recently = check_was_analyzed_recently(domain)
    was_analyzed_ever = check_was_analyzed_ever(domain)
    # print(was_analyzed_ever)
    # print(was_analyzed_recently)
    # print(f"target_domain: {domain}")
    if was_analyzed_recently:
        # print("1")
        return get_age_from_database(domain)
    elif was_analyzed_ever and force_upgrade:
        # print("2")
        return upgrade(domain, model)
    else:
        # print("3")
        ages = age_analyzer.get_friends_ages(domain)
        # print(domain)
        if ages == "PC" or not ages:
            return -1  # Profile closed
        estimated_age = model._query(ages)
        name = age_analyzer.get_name(domain)
        mean = round(st.mean(ages), 2)
        hmean = round(st.harmonic_mean(ages), 2)
        mode = round(neuroanalyzer.find_average_mode(ages), 2)
        median = round(st.median(ages), 2)
        std = round(neuroanalyzer.find_std(ages), 2)
        friends_cnt = len(ages)
        today = datetime.datetime.now()
        vk_age = age_analyzer.get_age(domain)
        query = (f"insert into analyzed("
                 f"id, domain, first_name, last_name, estimated_age, mean, mode, harmonic_mean,"
                 f"median, std, friends_cnt, verified, last_check, vk_age) values ("
                 f"{target_id}, \'{domain}\', \'{name['first_name']}\', \'{name['last_name']}\', {estimated_age}, {mean}, {mode}, {hmean}, {median},"
                 f"{std}, {friends_cnt}, False, current_date, {vk_age}"
                 f")")
        cur = connection.cursor()
        cur.execute(query)
        connection.commit()
        connection.close()
        # print(estimated_age)
        return estimated_age


def set_real_age(domain, real_age, verify):
    target_id = age_analyzer.get_id_by_domain(domain)
    domain = age_analyzer.get_domain_by_id(target_id)
    model = neuroanalyzer.AgeRegressor()
    model.open_model('neuronet.sav')
    analyze_and_insert(domain, model, force_upgrade=True)
    connection = psycopg2.connect(
        database=settings.db_name,
        user=settings.db_login,
        password=settings.db_pass,
        host=settings.db_ip,
        port=settings.db_port
    )
    cur = connection.cursor()
    cur.execute(f"UPDATE analyzed SET real_age = {real_age} WHERE id = \'{target_id}\';"
                f"UPDATE analyzed SET verified = {verify} WHERE id = \'{target_id}\';")
    connection.commit()
    connection.close()


def get_df_to_train():
    connection = psycopg2.connect(
        database=settings.db_name,
        user=settings.db_login,
        password=settings.db_pass,
        host=settings.db_ip,
        port=settings.db_port
    )
    cur = connection.cursor()
    cur.execute(f"SELECT real_age, mean, harmonic_mean, mode, median, std, friends_cnt from analyzed"
                f" where verified=True and abs(last_check-current_date) <= 1;")
    records = cur.fetchall()
    real_age_arr = []
    mean_arr = []
    hmean_arr = []
    mode_arr = []
    median_arr = []
    std_arr = []
    friends_cnt_arr = []
    for i in records:
        real_age_arr.append(i[0])
        mean_arr.append(i[1])
        hmean_arr.append(i[2])
        mode_arr.append(i[3])
        median_arr.append(i[4])
        std_arr.append((i[5]))
        friends_cnt_arr.append(i[6])
    df_raw = pd.DataFrame({
        "Real Age": real_age_arr,
        "Mean": mean_arr,
        "Harmonic Mean": hmean_arr,
        "Mode": mode_arr,
        "Median": median_arr,
        "std": std_arr,
        "Friends Count": friends_cnt_arr
    })
    return df_raw
