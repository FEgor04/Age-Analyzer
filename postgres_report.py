import datetime
import statistics as st

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
        ID integer, \
        DOMAIN varchar(250), \
        FIRST_NAME varchar(250), \
        LAST_NAME varchar(250), \
        ESTIMATED_AGE real, \
        REAL_AGE real, \
        MEAN real, \
        MODE real, \
        HARMONIC_MEAN real, \
        MEDIAN real, \
        STD real, \
        FRIENDS_CNT integer, \
        VERIFIED bool, \
        LAST_CHECK date \
    )')
    connection.commit()
    connection.close()


def upgrade(domain, model):
    connection = psycopg2.connect(
        database=settings.db_name,
        user=settings.db_login,
        password=settings.db_pass,
        host=settings.db_ip,
        port=settings.db_port
    )
    cur = connection.cursor()
    ages = age_analyzer.get_friends_ages(domain)
    estimated_age = model._query(ages)
    target_id = age_analyzer.get_id_by_domain(domain)
    name = age_analyzer.get_name(domain)
    mean = round(st.mean(ages), 2)
    hmean = round(st.harmonic_mean(ages), 2)
    mode = round(neuroanalyzer.find_average_mode(ages), 2)
    median = round(st.median(ages), 2)
    std = round(neuroanalyzer.find_std(ages), 2)
    friends_cnt = len(ages)
    query = (f"UPDATE analyzed SET estimated_age = {estimated_age} WHERE domain=\'{domain}\';"
             f"UPDATE analyzed SET mean = {mean} WHERE domain=\'{domain}\';"
             f"UPDATE analyzed SET harmonic_mean = {hmean} WHERE domain=\'{domain}\';"
             f"UPDATE analyzed SET mode = {mode} WHERE domain=\'{domain}\';"
             f"UPDATE analyzed SET median = {median} WHERE domain=\'{domain}\';"
             f"UPDATE analyzed SET std = {std} WHERE domain=\'{domain}\';"
             f"UPDATE analyzed SET last_check = current_date WHERE domain=\'{domain}\';"
             f"UPDATE analyzed SET friends_cnt = {friends_cnt} WHERE domain=\'{domain}\';"
             f"UPDATE analyzed SET first_name = \'{name['first_name']}\' WHERE domain=\'{domain}\';"
             f"UPDATE analyzed SET last_name = \'{name['last_name']}\' WHERE domain=\'{domain}\';"
             )
    cur.execute(query)
    connection.commit()
    connection.close()
    return estimated_age


def check_was_analyzed_recently(domain):
    connection = psycopg2.connect(
        database=settings.db_name,
        user=settings.db_login,
        password=settings.db_pass,
        host=settings.db_ip,
        port=settings.db_port
    )
    cur = connection.cursor()
    cur.execute(
        f"SELECT count(*) FROM analyzed WHERE domain=\'{domain}\' AND abs(last_check-current_date)<=1")
    records = cur.fetchall()
    connection.commit()
    connection.close()
    return records[0][0]


def check_was_analyzed_ever(domain):
    connection = psycopg2.connect(
        database=settings.db_name,
        user=settings.db_login,
        password=settings.db_pass,
        host=settings.db_ip,
        port=settings.db_port
    )
    cur = connection.cursor()
    cur.execute(
        f"SELECT count(*) FROM analyzed WHERE domain=\'{domain}\'")
    records = cur.fetchall()
    connection.commit()
    connection.close()
    return records[0][0]


def get_age_from_database(domain):
    connection = psycopg2.connect(
        database=settings.db_name,
        user=settings.db_login,
        password=settings.db_pass,
        host=settings.db_ip,
        port=settings.db_port
    )
    cur = connection.cursor()
    cur.execute(f"SELECT estimated_age FROM analyzed WHERE domain=\'{domain}\'")
    records = cur.fetchall()
    connection.commit()
    connection.close()
    if records == []:
        return 0
    else:
        return records[0][0]


def analyze_and_insert(domain, model, force_upgrade=False):
    connection = psycopg2.connect(
        database=settings.db_name,
        user=settings.db_login,
        password=settings.db_pass,
        host=settings.db_ip,
        port=settings.db_port
    )
    was_analyzed_recently = check_was_analyzed_recently(domain)
    was_analyzed_ever = check_was_analyzed_ever(domain)
    if was_analyzed_recently:
        return get_age_from_database(domain)
    elif was_analyzed_ever and force_upgrade:
        return upgrade(domain, model)
    else:
        ages = age_analyzer.get_friends_ages(domain)
        estimated_age = model._query(ages)
        target_id = age_analyzer.get_id_by_domain(domain)
        name = age_analyzer.get_name(domain)
        mean = round(st.mean(ages), 2)
        hmean = round(st.harmonic_mean(ages), 2)
        mode = round(neuroanalyzer.find_average_mode(ages), 2)
        median = round(st.median(ages), 2)
        std = round(neuroanalyzer.find_std(ages), 2)
        friends_cnt = len(ages)
        today = datetime.datetime.now()
        query = (f"insert into analyzed("
                 f"id, domain, first_name, last_name, estimated_age, mean, mode, harmonic_mean,"
                 f"median, std, friends_cnt, verified, last_check) values ("
                 f"{target_id}, \'{domain}\', \'{name['first_name']}\', \'{name['last_name']}\', {estimated_age}, {mean}, {mode}, {hmean}, {median},"
                 f"{std}, {friends_cnt}, {False}, current_date"
                 f")")
        cur = connection.cursor()
        cur.execute(query)
        connection.commit()
        connection.close()
        return estimated_age


def set_real_age(domain, real_age, verify):
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
    cur.execute(f"UPDATE analyzed SET real_age = {real_age} WHERE domain = \'{domain}\';"
                f"UPDATE analyzed SET verified = {verify} WHERE domain = \'{domain}\';")
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
    cur.execute(f"SELECT ")
