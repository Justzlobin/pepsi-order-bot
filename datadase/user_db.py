import psycopg2
from config import DB_TOKEN
from . import sqlite_db

conn = psycopg2.connect(DB_TOKEN, sslmode='require')
cur = conn.cursor()


def select_name_and_address_from_users(user_id):
    cur.execute("""SELECT user_full_name, user_address FROM users WHERE user_id = %s""", (user_id,))
    return cur.fetchall()


def check_user_for_registration(user_id):
    if user_id in sqlite_db.user_exist():
        return True
    else:
        return False


def register_or_update_user_data(user_id, value, name=False, address=False, register=False):
    if register:
        if name:
            cur.execute("""INSERT INTO users (user_id, user_full_name) VALUES (%s, %s)""", (user_id, value))
        if address:
            cur.execute("""INSERT INTO users (user_id, user_address) VALUES (%s, %s)""", (user_id, value))
    else:
        if name:
            cur.execute("""UPDATE users SET user_full_name = %s WHERE user_id = %s""", (value, user_id))
        if address:
            cur.execute("""UPDATE users SET user_address = %s WHERE user_id = %s""", (value, user_id))
    conn.commit()
    return True
