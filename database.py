from peewee import PostgresqlDatabase

import config


handler = PostgresqlDatabase(
    database=config.DATABASE_NAME,
    user=config.USERNAME,
    password=config.PASSWORD,
    host=config.DB_HOST
)


def fetchall(query):
    cursor = handler
    result = cursor.execute(query).fetchall()
    cursor.close()

    return result


def fetchone(query):
    cursor = handler
    result = cursor.execute(query).fetchone()
    cursor.close()

    return result

