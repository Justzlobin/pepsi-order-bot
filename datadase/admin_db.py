import psycopg2
from config import DB_TOKEN

conn = psycopg2.connect(DB_TOKEN, sslmode='require')
cur = conn.cursor()


def admin_select_product(brand_id) -> list:
    product_list = []
    cur.execute("""
                            SELECT brand_title, size, type, tasty_title, tasty_desc, pos_id
                            FROM position p, brand_cat b, size s, tasty t
                            WHERE p.brand_id = %s
                            AND p.brand_id = b.brand_id
                            AND p.size_id = s.size_id 
                            AND p.tasty_id = t.tasty_id
                            ORDER BY size 
                            """, (brand_id,))
    for i in cur.fetchall():
        product_list.append((i[5], f'{i[0]} {i[1]} {i[2]} {i[3]} {i[4]}'))
    return product_list


def check_in_status(value, pos_id):
    cur.execute("""UPDATE position SET in_stock = %s WHERE pos_id = %s""", (value, pos_id))
    return conn.commit()


def admin_select_one_position(pos_id):
    cur.execute("""SELECT brand_title, size, type, tasty_title, tasty_desc, price, in_stock
                            FROM position p, brand_cat b, size s, tasty t
                            WHERE p.pos_id = %s
                            AND p.brand_id = b.brand_id
                            AND p.size_id = s.size_id 
                            AND p.tasty_id = t.tasty_id""", (pos_id,))
    return cur.fetchone()
