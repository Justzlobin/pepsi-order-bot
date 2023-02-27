import psycopg2
from config import DB_TOKEN

conn = psycopg2.connect(DB_TOKEN, sslmode='require')
cur = conn.cursor()


def start_db():
    if conn:
        print('Data base connected OK!')


def user_exist(user_id) -> bool:
    cur.execute("SELECT user_id FROM users")
    list_users = cur.fetchall()
    if (user_id,) in list_users:
        return True
    else:
        return False


def select_all_categories() -> list:
    cur.execute("""SELECT * FROM category""")
    return cur.fetchall()


def select_brand(cat_id) -> list:
    cur.execute("""SELECT brand_id, brand_title FROM brand_cat WHERE cat_id = %s  ORDER BY brand_title""", (cat_id,))
    return cur.fetchall()


def select_position(brand_id):
    cur.execute("""             SELECT tasty_id , tasty_title
                                FROM   tasty
                                WHERE brand_id = %s  ORDER BY tasty_title""", (brand_id,))
    return cur.fetchall()


def select_product(brand_id) -> list:
    product_list = []
    cur.execute("""
                            SELECT brand_title, size, type, tasty_title, tasty_desc, pos_id
                            FROM position p, brand_cat b, size s, tasty t
                            WHERE p.brand_id = %s
                            AND p.brand_id = b.brand_id
                            AND p.size_id = s.size_id 
                            AND p.tasty_id = t.tasty_id
                            AND p.in_stock = %s
                            ORDER BY size 
                            """, (brand_id, True))
    for i in cur.fetchall():
        product_list.append((i[5], f'{i[0]} {i[1]} {i[2]} {i[3]} {i[4]}'))
    return product_list


def select_cat_id(brand_id):
    cur.execute("""SELECT cat_id FROM brand_cat WHERE brand_id = %s""", (brand_id,))
    return cur.fetchone()[0]


def select_brand_id(pos_id):
    print('pos ' + pos_id)
    cur.execute("""SELECT brand_id FROM position WHERE pos_id = %s""", (int(pos_id),))
    returned = cur.fetchone()[0]
    print(f'brand_id {returned}')
    return returned


def select_one_position(pos_id):
    cur.execute("""SELECT brand_title, size, type, tasty_title, tasty_desc, price, box_size
                            FROM position p, brand_cat b, size s, tasty t
                            WHERE p.pos_id = %s
                            AND p.brand_id = b.brand_id
                            AND p.size_id = s.size_id 
                            AND p.tasty_id = t.tasty_id""", (pos_id,))
    items = cur.fetchone()
    return {'brand_title': items[0], 'size': items[1], 'type': items[2], 'tasty_title': items[3],
            'tasty_desc': items[4], 'price': round(items[5], 2), 'box_size': items[6]}


def list_from_order(order_id, user_id):
    text_order_list = []
    text_order = select_from_order(order_id, user_id)
    for i in text_order:
        text_order_list.append(
            (i[5], f'{i[0]} {i[2]} {i[1]},\nК-ть:{str(i[3])}, Ціна: {str(i[4])}'))
    return text_order_list


def select_from_order(order_id, user_id):
    cur.execute("""SELECT DISTINCT brand_title, size, tasty_title, quantity, full_price, o.pos_id
                        FROM position p, brand_cat b, tasty t, "order" o, size s
                        WHERE o.order_id = %s
                        AND o.user_id = %s
                        AND p.brand_id = b.brand_id
                        AND p.tasty_id = t.tasty_id      
                        AND p.pos_id = o.pos_id
                        AND p.size_id = s.size_id 
                        """, (order_id, user_id))
    return cur.fetchall()


def sum_order(order_id) -> float:
    try:
        cur.execute("""SELECT SUM(full_price) FROM "order" WHERE order_id = %s""", (order_id,))
        return round(cur.fetchone()[0], 2)
    except TypeError:
        return 0


def select_multiplicity_and_box_size(pos_id):
    cur.execute("""SELECT multiplicity, box_size FROM size s, position p
                            WHERE p.pos_id = %s
                            AND p.size_id = s.size_id""", (pos_id,))
    return cur.fetchone()


def select_order_to_user_or_admin(order_id=None, admin=False):
    liste = []
    cur.execute("""
                SELECT  brand_title, tasty_title, size, quantity
                FROM position p, "order" o, brand_cat b, tasty t, size s
                WHERE o.order_id = %s 
                AND o.pos_id = p.pos_id 
                AND p.brand_id = b.brand_id
                AND p.tasty_id = t.tasty_id
                AND p.size_id = s.size_id
                """, (order_id,))
    text = cur.fetchall()
    for i in text:
        liste.append(f'{i[0]} {i[1]} {i[2]} - <b>{i[3]}</b> \n')
    comment = order_user_name_and_comment(order_id)
    if admin:
        liste.append(f'{comment[1]}\n'
                     f'{comment[2]}\n'
                     f'{comment[0]}\n')
    else:
        liste.append(f'{comment[1]}\n'
                     f'{comment[2]}\n')
    cur.execute("""SELECT SUM(full_price) FROM  "order" WHERE order_id= %s""", (order_id,))
    liste.append(
        f'Сумма: {cur.fetchone()[0]}'
        '\n')
    st = ''.join(liste)
    return st


def order_user_name_and_comment(order_id):
    cur.execute("""
                        SELECT user_full_name, comment, status FROM users, list
                        WHERE list.user_id = users.user_id
                        AND list.list_id = %s""", (order_id,))
    return cur.fetchone()


def select_last_order(user_id):
    cur.execute("""SELECT MAX(list_id) FROM list WHERE user_id = %s""", (user_id,))
    return cur.fetchone()[0]


def update_order_pos_id(quantity, order_id, pos_id):
    if quantity == 0:
        cur.execute("""DELETE FROM "order" WHERE order_id= %s AND pos_id= %s""", (order_id, pos_id))
        return conn.commit()
    else:
        cur.execute("""SELECT price FROM position WHERE pos_id = %s""", (pos_id,))
        amount = cur.fetchone()[0] * quantity
        cur.execute("""
                UPDATE "order"
                SET quantity = %s, full_price = %s
                WHERE order_id = %s
                AND pos_id = %s""", (quantity, amount, order_id, pos_id))
        return conn.commit()


def update_payment(user_id, payment):
    cur.execute("""UPDATE list SET payment = %s WHERE list_id = %s AND user_id = %s""",
                (payment, select_last_order(user_id), user_id))
    return conn.commit()


def list_order_to_admin():
    cur.execute("""SELECT list_id, user_full_name, date, payment
                    FROM list, users
                    WHERE list.user_id = users.user_id""")
    return cur.fetchall()[-20:]


def list_order_for_user(user_id):
    cur.execute("""SELECT date, order_id, SUM(full_price)
                    FROM list , "order" 
                    WHERE list.list_id = "order".order_id 
                    AND list.user_id = %s
                    GROUP BY list.date
                    
                    """, (user_id,))
    return cur.fetchall()


def update_order_state(order_id, state):
    cur.execute("""UPDATE list SET status = %s WHERE list_id = %s""", (state, order_id))
    return conn.commit()


def delete_order(order_id) -> bool:
    cur.execute("""SELECT status FROM list WHERE list_id = %s""", (order_id,))
    if cur.fetchone()[0] == '🕤 Очікування':
        cur.execute("""DELETE FROM list WHERE list_id = %s""", (order_id,))
        cur.execute("""DELETE FROM "order" WHERE order_id = %s""", (order_id,))
        conn.commit()
        return True
    else:
        return False


def select_price_of_box(pos_id, amount):
    cur.execute("""SELECT box_size FROM size s, position p WHERE 
                    p.size_id = s.size_id
                    AND p.pos_id = %s""", (pos_id,))
    box_size = cur.fetchone()[0]

    return round(amount / box_size, 1)


def save_order(user_id, order):
    def add_order_in_list():
        cur.execute("""INSERT INTO list (user_id, date, payment, comment) VALUES (%s, NOW(), %s, %s)""",
                    (user_id, order.order_settings_dict[user_id]['payment'],
                     order.order_settings_dict[user_id]['comment']))
        conn.commit()
        return True

    if add_order_in_list():
        cur.execute("""SELECT list_id FROM list WHERE user_id = %s""", (user_id,))
        order_id = cur.fetchall()[-1]
        for pos_id, quantity in order.order_dict[user_id].items():
            cur.execute("""SELECT price FROM position WHERE pos_id = %s""", (int(pos_id),))
            price = cur.fetchone()[0]
            cur.execute("""INSERT INTO "order" (pos_id, quantity, full_price, order_id ) VALUES (%s, %s, %s, %s)""",
                        (int(pos_id), quantity, price * quantity, order_id))
            conn.commit()
        return True


def close(self):
    self.close()
