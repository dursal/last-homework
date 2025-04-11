import sqlite3

def add_user(name, email, age):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", (name, email, age))
    conn.commit()
    conn.close()

def add_order(product, price):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (product, price) VALUES (?, ?)", (product, price))
    conn.commit()
    conn.close()

