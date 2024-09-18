from utils import env
from peewee import PostgresqlDatabase


handler = PostgresqlDatabase(
    database=env.get("DATABASE_NAME"),
    user=env.get("USER"),
    password=env.get("PASSWORD"),
    host=env.get("DATABASE_HOST")
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

