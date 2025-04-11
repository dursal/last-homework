import sqlite3
from db.db_utils import add_user, add_order

class TestDB:
    def test_user_in_db(self, setup_db):
            add_user("Аня", "anya@example.com", 17)
            conn = sqlite3.connect("test.db")
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE name = ?", ("Аня",))
            user = cursor.fetchone()

            assert user is not None, "Такого пользователя нет"
            assert user[1] == "Аня", "Имя не соответствует ожидаемому"
            assert user[2] == "anya@example.com", "Email не соответствует ожидаемому"
            assert user[3] == 17, "Возраст не соответствует ожидаемому"

    def test_user_in_db(self, setup_db):
            add_user("Аня", "anya@example.com", 17)
            conn = sqlite3.connect("test.db")
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE name = ?", ("Аня",))
            user = cursor.fetchone()

            assert user is not None, "Такого пользователя нет"
            assert user[1] == "Аня", "Имя не соответствует ожидаемому"
            assert user[2] == "anya@example.com", "Email не соответствует ожидаемому"
            assert user[3] == 17, "Возраст не соответствует ожидаемому"
