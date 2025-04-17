import pytest
import sqlite3

@pytest.fixture
def setup_db():
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    # Удаляем все данные (в нужном порядке, чтобы не нарушить внешние ключи)
    cursor.execute("DELETE FROM orders")
    cursor.execute("DELETE FROM users")

    # Создаём таблицы, если ещё нет
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
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()
    yield

@pytest.fixture(scope="session")
def base_url():
    return "https://reqres.in"

@pytest.fixture(scope="session")
def endpoint():
    return "/api/register"

@pytest.fixture
def url(base_url, endpoint):
    url = f"{base_url}{endpoint}"
    return url