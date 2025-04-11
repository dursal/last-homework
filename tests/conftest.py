import sqlite3
import pytest
import os

@pytest.fixture
def setup_db():
    if os.path.exists("test.db"):
        os.remove("test.db")
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        age INTEGER
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    product TEXT,
    price REAL,
    FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    conn.commit()
    conn.close()
    yield