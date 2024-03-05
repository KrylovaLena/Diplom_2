import pytest
import requests
import allure

from data import Urls as url
from data import Endpoints as ep


@allure.suite('Регистрация нового пользователя')
class TestRegisterUser:

    @allure.title("Создание уникального пользователя")
    @allure.description(" Тест на создание пользователя с валидными данными")
    def test_create_unique_user(self, registered_user_access_token):
        with allure.step("Шаг 1: Отправка POST-запроса на создание курьера"):
            response = registered_user_access_token
            email = response.json()["user"]["email"]
            name = response.json()["user"]["name"]
            access_token = response.json()["accessToken"]
            refresh_token = response.json()["refreshToken"]

        with allure.step("Шаг 2: Проверка кода ответа"):
            assert response.status_code == 200, "Ошибка: Неверный код ответа"
        with allure.step("Шаг 3: Проверка сообщения об успешном создании учетной записи с возвратом данных"):
            assert response.text == \
               f'{{"success":true,"user":{{"email":"{email}","name":"{name}"}},' \
               f'"accessToken":"{access_token}","refreshToken":"{refresh_token}"}}', "Ошибка: Создание учетной записи не удалось"


    @allure.title("Повторное создание уже зарегистрированного пользователя")
    @allure.description("Тест проверяет, что невозможно создать пользователя который уже зарегистрирован")
    def test_create_existing_user(self, register_new_user):
        data = register_new_user
        email = data[0]
        password = data[1]
        name = data[2]
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        with allure.step("Шаг 1: Отправка POST-запроса на создание пользователя"):
            request_url = f'{url.BASE_URL}{ep.CREATE_USER}'
            response = requests.post(request_url, data=payload)
        with allure.step("Шаг 2: Проверка кода ответа"):
            assert response.status_code == 403, "Ошибка: Неверный код ответа"
        with allure.step("Шаг 3: Проверка сообщения что пользователь не создан"):
            assert response.json()["success"] == False, "Ошибка: Неверное сообщение"
        with allure.step("Шаг 4: Проверка сообщения что пользователь уже зарегистрирован"):
            assert response.json()["message"] == "User already exists", "Ошибка: Неверное сообщение"


    @allure.title('Регистрация пользователя без обязательного поля {deleted_field}')
    @allure.description('Тест проверяет регистрацию пользователя с пустым обязательным полем {deleted_field}')
    @pytest.mark.parametrize('deleted_field', ['email', 'password', 'name'])
    def test_register_new_user_without_required_field(self, register_new_user, deleted_field):
        email = register_new_user[0]
        password = register_new_user[1]
        name = register_new_user[2]
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        del payload[deleted_field]
        with allure.step("Шаг 1: Отправка POST-запроса на создание пользователя с пустым обязательным полем {deleted_field}"):
            request_url = f'{url.BASE_URL}{ep.CREATE_USER}'
            response = requests.post(request_url, data=payload)
        with allure.step("Шаг 2: Проверка кода ответа"):
            assert response.status_code == 403
        with allure.step("Шаг 3: Проверка сообщения что заполнены не все обязательные поля"):
            assert response.text == '{"success":false,"message":"Email, password and name are required fields"}', "Ошибка: Неверное сообщение"
