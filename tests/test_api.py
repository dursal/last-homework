import pytest
import requests
import json
import allure

@allure.feature("Тестирование API")
class TestAPI:
    # Регистрация с валидными данными
    @allure.title("Регистрация с валидными данными")
    @allure.description("Ввести корректные логин и пароль и проверить, что запрос прошел успешно")
    @allure.severity(allure.severity_level.NORMAL)
    def test_valid(self, url):
        with allure.step("Ввести коректные данные и отправить запрос"):
            data= {
                "email": "eve.holt@reqres.in",
                 "password": "pistol"
            }
            response = requests.post(f"{url}", json=data)
        with allure.step("Проверить Status code"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        with allure.step("Убедиться, что тело ответа соответствует ожидаемому"):
            assert "id" in response.json(), "Ответ не содержит 'id'"
            assert response.json()["id"] == 4, "Значение 'id' не соответствует ожидаемому"
            assert "token" in response.json(), "Ответ не содержит 'token'"
            assert response.json()["token"] == "QpwL5tke4Pnpja7X4", "Значение 'token' не соответствует ожидаемому"

    # Без пароля
    @allure.title("Попытка регистрации без пароля")
    @allure.description("Пропустить ввод пароля и проверить, что вернулась ошибка")
    @allure.severity(allure.severity_level.NORMAL)
    def test_null_password(self, url):
        with allure.step("Пропустить ввод пароля и отправить запрос"):
            data= {
                "email": "sydney@fife"
            }
            response = requests.post(f"{url}", json=data)
        with allure.step("Проверить Status code"):
            assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
        with allure.step("Убедиться, что в ответе вернулось сообщение об ошибке"):
            assert "error" in response.json(), "Ответ не содержит 'error'"
            assert response.json()["error"] == "Missing password", "Значение 'error' не соответствует ожидаемому"

    # Без email
    @allure.title("Попытка регистрации без email")
    @allure.description("Пропустить ввод email и проверить, что вернулась ошибка")
    @allure.severity(allure.severity_level.NORMAL)
    def test_null_email(self, url):
        with allure.step("Пропустить ввод email и отправить запрос"):
            data= {
                "password": "pistol"
            }
            response = requests.post(f"{url}", json=data)
        with allure.step("Проверить Status code"):
            assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
        with allure.step("Убедиться, что в ответе вернулось сообщение об ошибке"):
            assert "error" in response.json(), "Ответ не содержит 'error'"
            assert response.json()["error"] == "Missing email or username", "Значение 'error' не соответствует ожидаемому"

    # Неверный email
    @allure.title("Попытка регистрации с некорректным email")
    @allure.description("Указать некорректный email и проверить, что вернулась ошибка")
    @allure.severity(allure.severity_level.NORMAL)
    def test_invalid_email(self, url):
        with allure.step("Указать некорректный email и отправить запрос"):
            data= {
                "email": "eve.holtreqres.in",
                 "password": "pistol"
            }
            response = requests.post(f"{url}", json=data)
        with allure.step("Проверить Status code"):
            assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
        with allure.step("Убедиться, что в ответе вернулось сообщение об ошибке"):
            assert "error" in response.json(), "Ответ не содержит 'error'"
            assert response.json()["error"] == "Note: Only defined users succeed registration", "Значение 'error' не соответствует ожидаемому"

    # Пустое тело запроса
    @allure.title("Попытка регистрации с пустыми полями")
    @allure.description("Отправить пустое тело запроса и проверить, что вернулась ошибка")
    @allure.severity(allure.severity_level.NORMAL)
    def test_null_data(self, url):
        with allure.step("Отправить пустое тело запроса"):
            data= {}
            response = requests.post(f"{url}", json=data)
        with allure.step("Проверить Status code"):
            assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
