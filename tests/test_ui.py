from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class TestIU:
    # Регистрация с валидными данными
    def test_valid(self):
        driver = webdriver.Chrome()

        # Открыть страницу с формой логина
        driver.get("https://demoqa.com/automation-practice-form")
        time.sleep(3)
        # Ввести имя
        firstname_input = driver.find_element(By.ID, "firstName")
        firstname_input.send_keys("Дарья")
        time.sleep(3)
        # Ввести фамилию
        lastname_input = driver.find_element(By.ID, "lastName")
        lastname_input.send_keys("Иванова")
        time.sleep(3)
        # Выбрать пол
        radio_button = driver.find_element(By.CSS_SELECTOR, "label[for='gender-radio-2']")
        radio_button.click()
        time.sleep(3)
        # Ввести номер
        usernumber_input = driver.find_element(By.ID, "userNumber")
        usernumber_input.send_keys("9106667711")
        time.sleep(3)
        # Нажать кнопку логина
        submit_button = driver.find_element(By.ID, "submit")
        submit_button.click()
        time.sleep(3)
        # Проверить, что вход выполнен успешно
        time.sleep(5)

        driver.quit()
