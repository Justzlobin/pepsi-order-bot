import psycopg2
from config import DB_TOKEN
from . import sqlite_db

conn = psycopg2.connect(DB_TOKEN, sslmode='require')
cur = conn.cursor()


def select_name_and_address_from_users(user_id):
    cur.execute("""SELECT user_full_name, user_address FROM users WHERE user_id = %s""", (user_id,))
    return cur.fetchall()


def check_user_for_registration(user_id):
    if str(user_id) in sqlite_db.user_exist():
        return True
    else:
        return False


def register_or_update_user_data(user_id, column_name, value, register=False):
    if register:
        cur.execute("""INSERT INTO users (%s) VALUES %s WHERE user_id = %s""", (column_name, value, user_id))
    else:
        cur.execute("""UPDATE users SET %s = %s WHERE user_id = %s""", (column_name, value, user_id))
    conn.commit()
    return True
