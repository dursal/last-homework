import pytest
import requests
import json

class TestAPI:
    # Регистрация с валидными данными
    def test_valid(self, url):
        data= {
            "email": "eve.holt@reqres.in",
             "password": "pistol"
        }
        response = requests.post(f"{url}", json=data)

        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        assert "id" in response.json(), "Ответ не содержит 'id'"
        assert response.json()["id"] == 4, "Значение 'id' не соответствует ожидаемому"
        assert "token" in response.json(), "Ответ не содержит 'token'"
        assert response.json()["token"] == "QpwL5tke4Pnpja7X4", "Значение 'token' не соответствует ожидаемому"

    # Без пароля
    def test_null_password(self, url):
        data= {
            "email": "sydney@fife"
        }
        response = requests.post(f"{url}", json=data)

        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
        assert "error" in response.json(), "Ответ не содержит 'error'"
        assert response.json()["error"] == "Missing password", "Значение 'error' не соответствует ожидаемому"

    # Без email
    def test_null_email(self, url):
        data= {
            "password": "pistol"
        }
        response = requests.post(f"{url}", json=data)

        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
        assert "error" in response.json(), "Ответ не содержит 'error'"
        assert response.json()["error"] == "Missing email or username", "Значение 'error' не соответствует ожидаемому"

    # Неверный email
    def test_invalid_email(self, url):
        data= {
            "email": "eve.holtreqres.in",
             "password": "pistol"
        }
        response = requests.post(f"{url}", json=data)

        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
        assert "error" in response.json(), "Ответ не содержит 'error'"
        assert response.json()["error"] == "Note: Only defined users succeed registration", "Значение 'error' не соответствует ожидаемому"

    # Пустое тело запроса
    def test_null_data(self, url):
        data= {}
        response = requests.post(f"{url}", json=data)

        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

    '''@pytest.mark.parametrize("p1, p2, p3, p4, p5, p6, p7",
                             [(-1000000, 0.1, 50, 5, 10, False, True),
                              (1000000, -0.1, 50, 5, 10, False, True),
                              (1000000, 0.1, -50, 5, 10, False, True),
                              (1000000, 0.1, 50, -5, 10, False, True),
                              (1000000, 0.1, 50, 5, -10, False, True),
                              (1000000, 0.1, 50, 0, 10, False, True),
                              (1000000, 0.1, 50, 5, 0, False, True),
                              (1000000, 0.1, 50, 15, 10, False, True)
                              ])
    def test_update_wave_config_negative(self, config_update_api, p1, p2, p3, p4, p5, p6, p7):'''