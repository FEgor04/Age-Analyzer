import psycopg2
import pytest

import neuroanalyzer
import postgres_report
import settings


def test_create_table():
    postgres_report.create_table()
    connection = psycopg2.connect(
        database=settings.db_name,
        user=settings.db_login,
        password=settings.db_pass,
        host=settings.db_ip,
        port=settings.db_port
    )
    cur = connection.cursor()
    cur.execute(
        "SELECT tablename FROM pg_catalog.pg_tables WHERE"
        " schemaname != 'pg_catalog' AND schemaname != 'information_schema';")
    records = cur.fetchall()
    flag: bool = False
    for i in records:
        if i[0] == "analyzed":
            flag = True
            break
    assert flag


@pytest.mark.parametrize("target, force_upgrade", [
    ("fegor2004", False),
    ("fegor2004", True),
    ("FASFSDASDSgsdsa", False)
])
def test_analyze_and_insert(target, force_upgrade):
    model = neuroanalyzer.AgeRegressor()
    model.open_model('neuronet.sav')
    postgres_report.analyze_and_insert(target, force_upgrade)
    assert True
