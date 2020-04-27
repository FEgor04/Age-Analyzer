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


def check_was_analyzed(domain):
    connection = psycopg2.connect(
        database=settings.db_name,
        user=settings.db_login,
        password=settings.db_pass,
        host=settings.db_ip,
        port=settings.db_port
    )
    cur = connection.cursor()
    cur.execute("SELECT count(*) FROM analyzed WHERE domain=\'{domain}\'")
    records = cur.fetchall()
    print(records)


def analyze_and_insert(domain, model):
    connection = psycopg2.connect(
        database=settings.db_name,
        user=settings.db_login,
        password=settings.db_pass,
        host=settings.db_ip,
        port=settings.db_port
    )
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
    # TODO: update if there are already some info about ID
    # print(cur)
    # print(name)
    today_str = today.strftime("%Y-%m-%d")
    print(today_str)
    query = (f"insert into analyzed("
             f"id, domain, first_name, last_name, estimated_age, mean, mode, harmonic_mean,"
             f"median, std, friends_cnt, verified, last_check) values ("
             f"{target_id}, \'{domain}\', \'{name['first_name']}\', \'{name['last_name']}\', {estimated_age}, {mean}, {mode}, {hmean}, {median},"
             f"{std}, {friends_cnt}, {False}, \'{today_str}\'"
             f")")
    print(query)
    cur = connection.cursor()
    cur.execute(query)
    connection.commit()
    connection.close()
    return estimated_age
