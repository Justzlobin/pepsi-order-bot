import sqlite3

conn = sqlite3.connect('C:\PepsiBot\datadase\pepsi_data.db')
cur = conn.cursor()

text = cur.execute("""SELECT * FROM position WHERE brand_id = 1""")
[print(f'brand_id: {i[0]}, tasty_id: {i[1]}, size_id: {i[2]}') for i in text]
