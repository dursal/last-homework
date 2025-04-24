from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import allure

@allure.feature("Тестирование UI")
class TestIU:
    @allure.title("Регистрация с валидными данными")
    @allure.description("Ввести валидные данные в поля регистрации и проверить, что регистрация прошла успешно")
    @allure.severity(allure.severity_level.NORMAL)
    # Ввод валидных данных в обязательные поля
    def test_valid(self):
        with allure.step("Открыть страницу с формой регистрации в браузере"):
            driver = webdriver.Chrome()
            # Открыть страницу с формой логина
            driver.get("https://demoqa.com/automation-practice-form")
        with allure.step("Ввести валидные данные в обязательные поля формы и нажать submit"):
            # Ввести имя
            driver.find_element(By.ID, "firstName").send_keys("Дарья")
            # Ввести фамилию
            driver.find_element(By.ID, "lastName").send_keys("Иванова")
            # Выбрать пол
            driver.find_element(By.CSS_SELECTOR, "label[for='gender-radio-2']").click()
            # Ввести номер
            driver.find_element(By.ID, "userNumber").send_keys("9106667711")
            # Нажать кнопку submit
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.find_element(By.ID, "submit").click()
            time.sleep(3)
        with allure.step("Проверить, что открылся алерт, подтверждающий регистрацию"):
            # Проверить, что осуществился переход на алерт с заполненной формой
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "modal-content"))
            )
            modal_title = driver.find_element(By.CLASS_NAME, "modal-header").text
            assert "Thanks for submitting the form" in modal_title
        with allure.step("Проверить, что значения в форме соответствуют введенным"):
            # Проверить, что значения в форме соответствуют введенным
            label_td = driver.find_element(By.XPATH, "//td[text()='Student Name']")
            value_td = label_td.find_element(By.XPATH, "following-sibling::td")
            name = value_td.text
            assert name == "Дарья Иванова", 'Имя добавлено некорректно'
            label_td = driver.find_element(By.XPATH, "//td[text()='Gender']")
            value_td = label_td.find_element(By.XPATH, "following-sibling::td")
            name = value_td.text
            assert name == "Female", 'Пол добавлен некорректно'
            label_td = driver.find_element(By.XPATH, "//td[text()='Mobile']")
            value_td = label_td.find_element(By.XPATH, "following-sibling::td")
            name = value_td.text
            assert name == "9106667711", 'Номер телефона добавлено некорректно'

        driver.quit()

    @allure.title("Регистрация с пустыми обязательными полями")
    @allure.description("Пропустить ввод обязательных полей и проверить, что возникла ошибка")
    @allure.severity(allure.severity_level.NORMAL)
    #Ошибка при незаполненных обязательных полях
    def test_empty_fields(self):
        with allure.step("Открыть страницу с формой регистрации в браузере"):
            driver = webdriver.Chrome()
            # Открыть страницу с формой логина
            driver.get("https://demoqa.com/automation-practice-form")
        with allure.step("Не заполняя обязательные поля, кликнуть submit"):
        # Нажать кнопку submit, не заполняя поля
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.find_element(By.ID, "submit").click()
            time.sleep(3)
        with allure.step("Проверить, что пустые обязательные поля подсветились красным"):
            # Проверяем, что пустые обязательные поля подсветились красным
            first_name_input = driver.find_element(By.ID, "firstName")
            border_color = first_name_input.value_of_css_property("border-color")
            assert border_color == "rgb(220, 53, 69)"
            lastName_input = driver.find_element(By.ID, "lastName")
            border_color = lastName_input.value_of_css_property("border-color")
            assert border_color == "rgb(220, 53, 69)"
            userNumber_input = driver.find_element(By.ID, "userNumber")
            border_color = userNumber_input.value_of_css_property("border-color")
            assert border_color == "rgb(220, 53, 69)"
            gender_radio_input = driver.find_element(By.CSS_SELECTOR, "label[for='gender-radio-1']")
            border_color = gender_radio_input.value_of_css_property("border-color")
            assert border_color == "rgb(220, 53, 69)"
            gender_radio_input = driver.find_element(By.CSS_SELECTOR, "label[for='gender-radio-2']")
            border_color = gender_radio_input.value_of_css_property("border-color")
            assert border_color == "rgb(220, 53, 69)"
            gender_radio_input = driver.find_element(By.CSS_SELECTOR, "label[for='gender-radio-3']")
            border_color = gender_radio_input.value_of_css_property("border-color")
            assert border_color == "rgb(220, 53, 69)"

        driver.quit()