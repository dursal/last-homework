import sqlite3
from db.db_utils import add_user, add_order, get_orders_by_user, delete_order, delete_user

class TestDB:
    #Добавить пользователя и проверить, что он есть в таблице users
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

            conn.commit()
            conn.close()

    #Добавить заказ для пользователя
    def test_order_in_db(self, setup_db):
            user_id = add_user(name="Аня", email="anya@example.com", age=17)
            add_order(user_id=user_id, product="Термос", price=5255)

            conn = sqlite3.connect("test.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM orders WHERE product = ?", ("Термос",))
            order = cursor.fetchone()

            assert order is not None, "Такого заказа нет"
            assert order[1] == user_id, f"Некорректный пользователь: {order[1]} != {user_id}"
            assert order[2] == "Термос", "Содержимое заказа не соответствует ожидаемому"
            assert order[3] == 5255, "Некорректная цена"

            conn.commit()
            conn.close()

    #Получить все заказы определённого пользователя
    def test_orders_by_user(self, setup_db):
            user_id = add_user(name="Валера", email="lera@example.com", age=37)
            add_order(user_id=user_id, product="Чайник", price=5255)
            add_order(user_id=user_id, product="Гироскутер", price=28132)
            add_order(user_id=user_id, product="Панамка", price=715)
            add_order(user_id=user_id, product="Электронасос", price=4250)
            add_order(user_id=user_id, product="Кофемашина", price=52800)

            orders = get_orders_by_user(user_id)

            assert len(orders) == 5, "Количество заказов не совпадает"
            assert ("Чайник", 5255) in orders, "Заказ на чайник не найден"
            assert ("Гироскутер", 28132) in orders, "Заказ на гироскутер не найден"
            assert ("Панамка", 715) in orders, "Заказ на панамку не найден"
            assert ("Электронасос", 4250) in orders, "Заказ на электронасос не найден"
            assert ("Кофемашина", 52800) in orders, "Заказ на кофемашину не найден"


    #Найти всех пользователей старше 18 лет
    def test_adult_users(self, setup_db):
            add_user("Игорь", "gora@example.com", 47)
            add_user("Наташа", "nat@example.com", 15)
            add_user("Вася", "vasya@example.com", 17)
            add_user("Кирилл", "kira@example.com", 19)
            add_user("Настя", "st@example.com", 11)
            add_user("Антон", "antoni@example.com", 21)

            conn = sqlite3.connect("test.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE age > 18")
            orders = cursor.fetchall()

            assert len(orders) == 3

            names = [user[1] for user in orders]
            assert "Игорь" in names, "Игорь тоже совершеннолетний"
            assert "Кирилл" in names, "Кирилл тоже совершеннолетний"
            assert "Антон" in names, "Антон тоже совершеннолетний"

    #Найти сумму всех заказов по user_id
    def test_sum_prices(self, setup_db):
            user_id = add_user(name="Валера", email="lera@example.com", age=37)
            add_order(user_id=user_id, product="Чайник", price=5255)
            add_order(user_id=user_id, product="Гироскутер", price=28132)
            add_order(user_id=user_id, product="Панамка", price=715)
            add_order(user_id=user_id, product="Электронасос", price=4250)
            add_order(user_id=user_id, product="Кофемашина", price=52800)

            conn = sqlite3.connect("test.db")
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(price) FROM orders WHERE user_id = ?", (user_id,))
            summ = cursor.fetchone()[0]

            assert summ == 5255+28132+715+4250+52800, "Сумма заказов неверна"

    #Удалить заказ и убедиться, что он пропал
    def test_delete_order(self, setup_db):
            user_id = add_user(name="Валера", email="lera@example.com", age=37)
            add_order(user_id=user_id, product="Чайник", price=5255)
            add_order(user_id=user_id, product="Гироскутер", price=28132)

            orders = get_orders_by_user(user_id)

            assert len(orders) == 2, "Количество заказов не совпадает"
            assert ("Чайник", 5255) in orders, "Заказ на чайник не найден"
            assert ("Гироскутер", 28132) in orders, "Заказ на гироскутер не найден"

            delete_order("Чайник")
            orders = get_orders_by_user(user_id)

            assert len(orders) == 1, "Количество заказов не совпадает"
            assert ("Чайник", 5255) not in orders, "Заказ на чайник не найден"
            assert ("Гироскутер", 28132) in orders, "Заказ на гироскутер не найден"

    #Удалить пользователя (опционально — и связанные заказы)
    def test_delete_user(self, setup_db):
            user_id = add_user("Валера", "lera@example.com", 37)
            add_order(user_id=user_id, product="Чайник", price=5255)
            conn = sqlite3.connect("test.db")
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users")
            user = cursor.fetchone()

            assert user is not None, "Пользователь не добавлен"
            assert user[1] == "Валера", "Имя не соответствует ожидаемому"

            orders = get_orders_by_user(user_id)

            assert ("Чайник", 5255) in orders, "Заказ на чайник не найден"

            delete_user(user_id, True)
            cursor.execute("SELECT * FROM users")
            user = cursor.fetchone()
            assert user is None, "Пользователь не удален"
            orders = get_orders_by_user(user_id)
            assert ("Чайник", 5255) not in orders, "Заказ на чайник не удален"












