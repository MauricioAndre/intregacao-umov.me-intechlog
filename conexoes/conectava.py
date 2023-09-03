import psycopg2

import os
import dotenv

dotenv.load_dotenv()


def conecta(query):


    host = os.getenv("HOST")
    database = os.getenv("DATABASE")
    port = os.getenv("PORT")
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")


    connection = psycopg2.connect(host=host, database=database, port=port, user=user, password=password)
    cursor = connection.cursor()

    cursor.execute(query)
    result = cursor.fetchall()
    return result

