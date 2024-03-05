import pytest
import requests
import allure

from data import Urls as url
from data import Endpoints as ep


@allure.suite('Авторизация пользователя')
class TestAuthUser:
    @allure.title('Авторизация пользователя со всеми заполненными обязательными полями')
    @allure.description('Тест проверяет успешную авторизацию зарегистрированного пользователя')
    def test_login_user(self, register_new_user):
        email = register_new_user[0]
        password = register_new_user[1]

        payload = {
            "email": email,
            "password": password
        }
        with allure.step("Шаг 1: Отправка POST-запроса на авторизацию пользователя"):
            request_url = f'{url.BASE_URL}{ep.LOGIN_USER}'
            response = requests.post(request_url, data=payload)
        with allure.step("Шаг 2: Проверка кода ответа"):
            assert response.status_code == 200, "Ошибка: Неверный код ответа"
        with allure.step("Шаг 3: Проверка сообщения что пользователь авторизован"):
            assert response.json()['success'] == True, "Ошибка: Неверное сообщение"

    @allure.title('Авторизация пользователя без обязательного поля {deleted_field}')
    @allure.description('Тест проверяет авторизацию пользователя с пустым обязательным полем {deleted_field}')
    @pytest.mark.parametrize('deleted_field', ['email', 'password'])
    def test_login_user_without_required_field(self, register_new_user, deleted_field):
        email = register_new_user[0]
        password = register_new_user[1]
        payload = {
            "email": email,
            "password": password
        }
        del payload[deleted_field]
        with allure.step("Шаг 1: Отправка POST-запроса на авторизацию пользователя с пустым обязательным полем {deleted_field}"):
            request_url = f'{url.BASE_URL}{ep.LOGIN_USER}'
            response = requests.post(request_url, data=payload)
        with allure.step("Шаг 2: Проверка кода ответа"):
            assert response.status_code == 401, "Ошибка: Неверный код ответа"
        with allure.step("Шаг 3: Проверка сообщения что заполнены не все обязательные поля"):
            assert response.text == '{"success":false,"message":"email or password are incorrect"}', "Ошибка: Неверное сообщение"


    @allure.title('Авторизация пользователя с некорректным password')
    @allure.description('Тест проверяет авторизацию пользователя с неправильно заполненным password')
    def test_login_user_without_password(self, register_new_user):
        email = register_new_user[0]
        password = 'password123'
        payload = {
            "email": email,
            "password": password
        }
        with allure.step("Шаг 1: Отправка POST-запроса на авторизацию пользователя с корректным email, но некорректным password"):
            request_url = f'{url.BASE_URL}{ep.LOGIN_USER}'
            response = requests.post(request_url, data=payload)
        with allure.step("Шаг 2: Проверка кода ответа"):
            assert response.status_code == 401, "Ошибка: Неверный код ответа"
        with allure.step("Шаг 3: Проверка сообщения что заполнены не все обязательные поля"):
            assert response.text == '{"success":false,"message":"email or password are incorrect"}', "Ошибка: Неверное сообщение"


    @allure.title('Авторизация пользователя с некорректным email')
    @allure.description('Тест проверяет авторизацию пользователя с неправильно заполненным email')
    def test_login_user_without_email(self, register_new_user):
        email = 'email123'
        password = register_new_user[1]
        payload = {
            "email": email,
            "password": password
        }
        with allure.step("Шаг 1: Отправка POST-запроса на авторизацию пользователя с корректным password, но некорректным email"):
            request_url = f'{url.BASE_URL}{ep.LOGIN_USER}'
            response = requests.post(request_url, data=payload)
        with allure.step("Шаг 2: Проверка кода ответа"):
            assert response.status_code == 401, "Ошибка: Неверный код ответа"
        with allure.step("Шаг 3: Проверка сообщения что заполнены не все обязательные поля"):
            assert response.text == '{"success":false,"message":"email or password are incorrect"}', "Ошибка: Неверное сообщение"
