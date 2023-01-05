import psycopg2
from config import DB_TOKEN

conn = psycopg2.connect(DB_TOKEN, sslmode='require')
cur = conn.cursor()


def select_name_and_address_from_users(user_id):
    cur.execute("""SELECT user_full_name, user_address FROM users WHERE user_id = %s""", (user_id,))
    return cur.fetchall()
