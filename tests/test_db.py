import sqlite3
import allure
from db.db_utils import add_user, add_order, get_orders_by_user, delete_order, delete_user

@allure.feature("Тестирование базы данных")
class TestDB:
    #Добавить пользователя и проверить, что он есть в таблице users
    @allure.title("Добавление пользователя")
    @allure.description("Добавить пользователя и проверить, что он есть в таблице users")
    @allure.severity(allure.severity_level.NORMAL)
    def test_user_in_db(self, setup_db):
            with allure.step("Добавить пользователя в таблицу"):
                    add_user("Аня", "anya@example.com", 17)
                    conn = sqlite3.connect("test.db")
                    cursor = conn.cursor()
            with allure.step("Найти пользователя с указанным именем"):
                    cursor.execute("SELECT * FROM users WHERE name = ?", ("Аня",))
                    user = cursor.fetchone()
            with allure.step("Проверить, что таблица не пуста"):
                    assert user is not None, "Такого пользователя нет"
            with allure.step("Проверить, что имя соответствует ожидаемому"):
                    assert user[1] == "Аня", "Имя не соответствует ожидаемому"
            with allure.step("Проверить, что email соответствует ожидаемому"):
                    assert user[2] == "anya@example.com", "Email не соответствует ожидаемому"
            with allure.step("Проверить, что возраст соответствует ожидаемому"):
                    assert user[3] == 17, "Возраст не соответствует ожидаемому"

            conn.commit()
            conn.close()

    #Добавить заказ для пользователя
    @allure.title("Добавление заказа")
    @allure.description("Добавить заказ для пользователя и проверить, что он успешно добавлен")
    @allure.severity(allure.severity_level.NORMAL)
    def test_order_in_db(self, setup_db):
            with allure.step("Добавить пользователя в таблицу"):
                    user_id = add_user(name="Аня", email="anya@example.com", age=17)
            with allure.step("Добавить заказ для пользователя"):
                    add_order(user_id=user_id, product="Термос", price=5255)
            with allure.step("Найти заказ по названию"):
                    conn = sqlite3.connect("test.db")
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM orders WHERE product = ?", ("Термос",))
                    order = cursor.fetchone()
            with allure.step("Проверить, что таблица заказов не пуста"):
                    assert order is not None, "Такого заказа нет"
            with allure.step("Проверить, что id заказа соответствует id пользователя"):
                    assert order[1] == user_id, f"Некорректный пользователь: {order[1]} != {user_id}"
            with allure.step("Проверить, что содержимое заказа соответствует ожидаемому"):
                    assert order[2] == "Термос", "Содержимое заказа не соответствует ожидаемому"
            with allure.step("Проверить, что цена заказа корректна"):
                    assert order[3] == 5255, "Некорректная цена"

            conn.commit()
            conn.close()

    #Получить все заказы определённого пользователя
    @allure.title("Получение заказов пользователя")
    @allure.description("Получить все заказы определённого пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    def test_orders_by_user(self, setup_db):
            with allure.step("Добавить пользователя"):
                    user_id = add_user(name="Валера", email="lera@example.com", age=37)
            with allure.step("Добавить заказы для пользователя"):
                    add_order(user_id=user_id, product="Чайник", price=5255)
                    add_order(user_id=user_id, product="Гироскутер", price=28132)
                    add_order(user_id=user_id, product="Панамка", price=715)
                    add_order(user_id=user_id, product="Электронасос", price=4250)
                    add_order(user_id=user_id, product="Кофемашина", price=52800)

            with allure.step("Получить заказы указанного пользователя"):
                    orders = get_orders_by_user(user_id)
            with allure.step("Проверить, что количество заказов совпадает"):
                    assert len(orders) == 5, "Количество заказов не совпадает"
            with allure.step("Проверить, что все добавленные заказы сохранены с соответствующей ценой"):
                    assert ("Чайник", 5255) in orders, "Заказ на чайник не найден"
                    assert ("Гироскутер", 28132) in orders, "Заказ на гироскутер не найден"
                    assert ("Панамка", 715) in orders, "Заказ на панамку не найден"
                    assert ("Электронасос", 4250) in orders, "Заказ на электронасос не найден"
                    assert ("Кофемашина", 52800) in orders, "Заказ на кофемашину не найден"


    #Найти всех пользователей старше 18 лет
    @allure.title("поиск пользователей")
    @allure.description("Найти всех пользователей старше 18 лет")
    @allure.severity(allure.severity_level.NORMAL)
    def test_adult_users(self, setup_db):
            with allure.step("Добавить несколько пользователей"):
                    add_user("Игорь", "gora@example.com", 47)
                    add_user("Наташа", "nat@example.com", 15)
                    add_user("Вася", "vasya@example.com", 17)
                    add_user("Кирилл", "kira@example.com", 19)
                    add_user("Настя", "st@example.com", 11)
                    add_user("Антон", "antoni@example.com", 21)

            with allure.step("Найти пользователей старше 18 и проверить количество"):
                    conn = sqlite3.connect("test.db")
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM users WHERE age > 18")
                    orders = cursor.fetchall()

                    assert len(orders) == 3

            with allure.step("Проверить,что найдены все пользователи старше 18"):
                    names = [user[1] for user in orders]
                    assert "Игорь" in names, "Игорь тоже совершеннолетний"
                    assert "Кирилл" in names, "Кирилл тоже совершеннолетний"
                    assert "Антон" in names, "Антон тоже совершеннолетний"

    #Найти сумму всех заказов по user_id
    @allure.title("Поиск суммы заказов пользователя")
    @allure.description("Найти сумму всех заказов по user_id")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sum_prices(self, setup_db):
            with allure.step("Добавить пользователя"):
                    user_id = add_user(name="Валера", email="lera@example.com", age=37)
            with allure.step("Добавить несколько заказов пользователю"):
                    add_order(user_id=user_id, product="Чайник", price=5255)
                    add_order(user_id=user_id, product="Гироскутер", price=28132)
                    add_order(user_id=user_id, product="Панамка", price=715)
                    add_order(user_id=user_id, product="Электронасос", price=4250)
                    add_order(user_id=user_id, product="Кофемашина", price=52800)

            with allure.step("Найти сумму заказов пользователя и проверить, что сумма корректна"):
                    conn = sqlite3.connect("test.db")
                    cursor = conn.cursor()
                    cursor.execute("SELECT SUM(price) FROM orders WHERE user_id = ?", (user_id,))
                    summ = cursor.fetchone()[0]

                    assert summ == 5255+28132+715+4250+52800, "Сумма заказов неверна"

    #Удалить заказ и убедиться, что он пропал
    @allure.title("Удаление заказа")
    @allure.description("Удалить заказ и убедиться, что он пропал")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_order(self, setup_db):
            with allure.step("Добавить пользователя"):
                    user_id = add_user(name="Валера", email="lera@example.com", age=37)
            with allure.step("Добавить несколько заказов пользователю"):
                    add_order(user_id=user_id, product="Чайник", price=5255)
                    add_order(user_id=user_id, product="Гироскутер", price=28132)

            with allure.step("Проверить количество заказов пользователя"):
                    orders = get_orders_by_user(user_id)
                    assert len(orders) == 2, "Количество заказов не совпадает"
            with allure.step("Проверить, что заказы соответствуют добавленным"):
                    assert ("Чайник", 5255) in orders, "Заказ на чайник не найден"
                    assert ("Гироскутер", 28132) in orders, "Заказ на гироскутер не найден"

            with allure.step("Удалить один заказ"):
                    delete_order("Чайник")
            with allure.step("Получить список заказов и убедиться, что соответствующий заказ удален"):
                    orders = get_orders_by_user(user_id)
                    assert len(orders) == 1, "Количество заказов не совпадает"
                    assert ("Чайник", 5255) not in orders, "Заказ на чайник не найден"
                    assert ("Гироскутер", 28132) in orders, "Заказ на гироскутер не найден"

    #Удалить пользователя (опционально — и связанные заказы)
    @allure.title("Удаление пользователя")
    @allure.description("Удалить пользователя и его заказы")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_user(self, setup_db):
            with allure.step("Добавить пользователя"):
                    user_id = add_user("Валера", "lera@example.com", 37)
            with allure.step("Добавить заказ пользователю"):
                    add_order(user_id=user_id, product="Чайник", price=5255)
                    conn = sqlite3.connect("test.db")
                    cursor = conn.cursor()

            with allure.step("Проверить, что соответствующий пользователь добавлен"):
                    cursor.execute("SELECT * FROM users")
                    user = cursor.fetchone()
                    assert user is not None, "Пользователь не добавлен"
                    assert user[1] == "Валера", "Имя не соответствует ожидаемому"

            with allure.step("Проверить, что соответствующий заказ добавлен"):
                    orders = get_orders_by_user(user_id)
                    assert ("Чайник", 5255) in orders, "Заказ на чайник не найден"

            with allure.step("Удалить пользователя и его заказы"):
                    delete_user(user_id, True)
            with allure.step("Проверить, что пользователь удален"):
                    cursor.execute("SELECT * FROM users")
                    user = cursor.fetchone()
                    assert user is None, "Пользователь не удален"
            with allure.step("Проверить, что заказ удален"):
                    orders = get_orders_by_user(user_id)
                    assert ("Чайник", 5255) not in orders, "Заказ на чайник не удален"












