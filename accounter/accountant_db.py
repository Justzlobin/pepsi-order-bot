import psycopg2
from config import DB_TOKEN

conn = psycopg2.connect(DB_TOKEN, sslmode='require')
cur = conn.cursor()


def accountant_add_record_in_db(text):
    record = text.split()
    print(record)
    cur.execute(
        """INSERT INTO accountant (type_record, value_record, desc_record, time_record)
         VALUES (%s, %s, %s, NOW())""",
        (record[0], record[1], record[2]))
    conn.commit()
    return True


def sum_record():
    cur.execute("SELECT * FROM accountant")
    return str(cur.fetchall())


def close(self):
    self.close()
