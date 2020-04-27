import psycopg2

import settings

connection = psycopg2.connect(
    database=settings.db_name,
    user=settings.db_login,
    password=settings.db_pass,
    host=settings.db_ip,
    port=settings.db_port
)


def query():
    pass
