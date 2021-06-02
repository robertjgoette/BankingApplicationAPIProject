from psycopg2 import connect
from psycopg2._psycopg import OperationalError
import os


def create_connection():
    try:
        conn = connect(
            host= os.environ.get('HOST'),
            database=os.environ.get('DB'),
            user=os.environ.get('USER'),
            password=os.environ.get('PW'),
            port=os.environ.get('PORT')
        )
        return conn
    except OperationalError as e:
        print(e)


connection = create_connection()
