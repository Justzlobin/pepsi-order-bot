import psycopg2
from config import DB_TOKEN

conn = psycopg2.connect(DB_TOKEN, sslmode='require')
cur = conn.cursor()


def start_db():
    if conn:
        print('Data base connected OK!')


def user_exist():
    return [i[0] for i in cur.execute("SELECT user_id FROM users").fetchall()]


def get_user_id(user_id):
    result = cur.execute("SELECT id FROM users WHERE 'user_id' = ?", (user_id,))
    return result.fetchone()[0]


async def add_user(state, user_id):
    async with state.proxy() as data:
        val = data.values()
        if user_id not in user_exist():
            cur.execute("INSERT INTO 'users' (user_id, user_full_name, user_address) VALUES (?, ?, ?)",
                        (user_id, tuple(val)[0],
                         tuple(val)[1]))
        else:
            cur.execute("""UPDATE users
            SET  user_full_name = ?, user_address = ?
            WHERE user_id = ?""", (tuple(val)[0], tuple(val)[1], user_id))
        print(val)
        return conn.commit()


def add_position_in_order(id, user_value, position):
    cur.execute("""INSERT INTO 'order' ('order_id', 'quantity', 'position' ) VALUES (?,?,?) """,
                (id, int(user_value), str(position)))
    conn.commit()


def select_all_categories():
    return cur.execute("""SELECT * FROM category""").fetchall()


def select_brand(cat_id) -> list:
    brands = cur.execute("""
                            SELECT brand_id, brand_title FROM brand_cat 
                             WHERE   cat_id = (?)""", (cat_id,)).fetchall()
    return brands


def select_position(brand_id):
    positions = cur.execute("""
                                SELECT tasty_id , tasty_title
                                FROM   tasty
                                WHERE brand_id = (?)""", (brand_id,)).fetchall()
    return positions


def select_product(brand_id) -> list:
    product_list = []
    product = cur.execute("""
                            SELECT brand_title, size, type, tasty_title, tasty_desc, pos_id
                            FROM position p, brand_cat b, size s, tasty t
                            WHERE p.brand_id = (?)
                            AND p.brand_id = b.brand_id
                            AND p.size_id = s.size_id 
                            AND p.tasty_id = t.tasty_id

                            """, (brand_id,)).fetchall()
    for i in product:
        product_list.append((i[5], f'{i[0]} {i[1]} {i[2]} {i[3]} {i[4]}'))
    return product_list


def select_cat_id(brand_id):
    return cur.execute("""SELECT cat_id FROM brand_cat WHERE brand_id = (?)""", (brand_id,)).fetchone()[0]


def select_brand_id(pos_id):
    return cur.execute("""SELECT brand_id FROM position WHERE pos_id = (?)""", (pos_id,)).fetchone()[0]


def select_one_position(pos_id):
    position = cur.execute("""SELECT brand_title, size, type, tasty_title, tasty_desc, price
                            FROM position p, brand_cat b, size s, tasty t
                            WHERE p.pos_id = (?)
                            AND p.brand_id = b.brand_id
                            AND p.size_id = s.size_id 
                            AND p.tasty_id = t.tasty_id""", (pos_id,)).fetchone()

    return position


def add_in_order(order_id, pos_id, quantity, price, user_id):
    if quantity != 0:
        cur.execute("""INSERT INTO 'order' ('order_id', pos_id, quantity, full_price, user_id)
                VALUES (?,?,?,?,?)  """,
                    (order_id, pos_id, quantity, price, user_id))
        conn.commit()


def list_from_order(order_id, user_id):
    text_order_list = []
    text_order = select_from_order(order_id, user_id)
    for i in text_order:
        text_order_list.append(
            (i[5], f'Бренд: {i[0]}, Смак: {i[2]}, Розмір: {i[1]},\nК-ть:{str(i[3])}, Ціна: {str(i[4])}'))
    return text_order_list


def select_from_order(order_id, user_id):
    lis = cur.execute("""SELECT DISTINCT brand_title, size, tasty_title, quantity, full_price, 'order'.pos_id
                        FROM position p, brand_cat b, tasty t, 'order', size s
                        WHERE 'order'.'order_id' = (?)
                        AND 'order'.user_id = (?)
                        AND p.brand_id = b.brand_id
                        AND p.tasty_id = t.tasty_id      
                        AND p.pos_id = 'order'.pos_id
                        AND p.size_id = s.size_id 
                        """, (order_id, user_id)).fetchall()
    return lis


def add_in_list_orders(order_id, user_id):
    cur.execute("""
                    INSERT INTO list
                    VALUES (?,?, CURDATE())""",
                (order_id, user_id))
    conn.commit()


def check_list_order_id():
    order_id = cur.execute("""SELECT list_id FROM list """).fetchall()[-1][0]
    return order_id


def select_address_from_users(user_id):
    return cur.execute("""SELECT user_address FROM users WHERE user_id = (?)""", (user_id,)).fetchall()


def create_new_custom(user_id):
    new_custom = check_list_order_id() + 1
    cur.execute("""INSERT INTO list (list_id, user_id) VALUES (?,?)""",
                (new_custom, user_id))
    conn.commit()
    return new_custom


def delete_from_order(order_id):
    cur.execute("""DELETE FROM 'order' WHERE order_id = (?)""", (order_id,))
    cur.execute("""DELETE FROM list WHERE list_id = (?)""", (order_id,))
    return conn.commit()


def sum_order(order_id) -> float:
    try:
        return round(
            cur.execute("""SELECT SUM(full_price) FROM 'order' WHERE order_id =(?)""", (order_id,)).fetchone()[0],
            2)
    except TypeError:
        return 0


def select_multiplicity_and_box_size(pos_id):
    return cur.execute("""SELECT multiplicity, box_size FROM size s, position p
                            WHERE p.pos_id = (?)
                            AND p.size_id = s.size_id""", (pos_id,)).fetchone()


def select_order_to_admin(order_id):
    liste = []
    text = cur.execute("""
                SELECT  brand_title, tasty_title, size, quantity
                FROM position p, 'order' o, brand_cat b, tasty t, size s
                WHERE o.order_id = ? 
                AND o.pos_id = p.pos_id 
                AND p.brand_id = b.brand_id
                AND p.tasty_id = t.tasty_id
                AND p.size_id = s.size_id
                """, (order_id,)).fetchall()
    for i in text:
        liste.append(f'{i[0]} {i[1]} {i[2]} - <b>{i[3]}</b> \n')
    for l in order_user_name_and_comment(order_id):
        liste.append(f'{l}\n')
    liste.append(
        f'Сумма: {cur.execute("""SELECT SUM(full_price) FROM "order" WHERE order_id=(?)""", (order_id,)).fetchone()[0]}'
        '\n')
    liste.append(f'Номер: {order_id}')
    st = ''.join(liste)
    return st


def order_user_name_and_comment(order_id):
    return cur.execute("""
                        SELECT user_full_name, comment, status FROM users, list
                        WHERE list.user_id = users.user_id
                        AND list.list_id = (?)""", (order_id,)).fetchone()


def select_last_order(user_id):
    return cur.execute("""SELECT MAX(list_id) FROM list WHERE user_id = (?)""", (user_id,)).fetchone()[0]


#
def last_order(user_id) -> list:
    text = cur.execute("""
            SELECT order_pos_id, brand_title, tasty_title, size, quantity, full_price
            FROM 'order' o, brand_cat b, tasty t, size s, position p
            WHERE order_id = (SELECT MAX(order_id) FROM 'order' WHERE user_id = (?))
            AND o.pos_id = p.pos_id 
                AND p.brand_id = b.brand_id
                AND p.tasty_id = t.tasty_id
                AND p.size_id = s.size_id
             """, (user_id,)).fetchall()

    return [list((a[0], f'{a[1]} {a[2]} {a[3]} {a[4]}', round(a[5]))) for a in text]


def update_order_pos_id(quantity, order_id, pos_id):
    if quantity == 0:
        cur.execute("""DELETE FROM 'order' WHERE order_id=(?) AND pos_id=(?)""", (order_id, pos_id))
        return conn.commit()
    else:
        amount = cur.execute("""SELECT price FROM position WHERE pos_id = (?)""", (pos_id,)).fetchone()[0] * quantity
        cur.execute("""
                UPDATE 'order'
                SET quantity = (?), full_price = (?)
                WHERE order_id = (?)
                AND pos_id = (?)""", (quantity, amount, order_id, pos_id))
        return conn.commit()


def update_payment(user_id, payment):
    cur.execute("""UPDATE list SET payment = (?) WHERE list_id = (?) AND user_id = (?)""",
                (payment, select_last_order(user_id), user_id))
    return conn.commit()


async def update_comment(user_id, state):
    async with state.proxy() as data:
        dit = data.values()
        print(dit)
    cur.execute("""UPDATE list SET comment = (?) WHERE list_id = (?) AND user_id = (?)""",
                (tuple(dit)[0], select_last_order(user_id), user_id))

    return conn.commit()


def list_order_to_admin():
    return cur.execute("""SELECT list_id, user_full_name, date, payment
                    FROM list, users
                    WHERE list.user_id = users.user_id""").fetchall()


def list_order_to_user(user_id):
    return cur.execute("""SELECT date, payment, list_id
                        FROM list l 
                        WHERE l.user_id = (?)
                        """, (user_id,)).fetchall()


def update_order_state(order_id, state):
    cur.execute("""UPDATE list SET status = (?) WHERE list_id = (?)""", (state, order_id))
    return conn.commit()


def close(self):
    self.close()
