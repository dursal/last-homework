import sqlite3

def add_user(name, email, age):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", (name, email, age))
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return user_id

def add_order(user_id, product, price):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (user_id, product, price) VALUES (?, ?, ?)", (user_id, product, price))
    conn.commit()
    conn.close()

def get_orders_by_user(user_id):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    cursor.execute("SELECT product, price FROM orders WHERE user_id = ?", (user_id,))
    orders = cursor.fetchall()

    conn.close()
    return orders

def delete_order(product):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE product = ?", (product,))
    conn.commit()
    conn.close()


def delete_user(user_id, delete_orders=False):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    if delete_orders:
        cursor.execute("DELETE FROM orders WHERE user_id = ?", (user_id,))

    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))

    conn.commit()
    conn.close()

