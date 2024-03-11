import allure
import pytest
import requests
from faker import Faker

from data import Urls as url
from data import Endpoints as ep


@allure.suite('Изменение данных пользователя')
class TestUpdateUser:

    @allure.title('Изменение данных авторизованного пользователя')
    @allure.description('Тест на изменение поля {update_data} у авторизованного пользователя')
    @pytest.mark.parametrize('update_data', ['{"email": fake.email(), "password": data[1],"name": data[2]}',
                                              '{"email": data[0], "password": fake.password(), "name": data[2]}',
                                              '{"email": data[0], "password":data[1], "name":fake.name()}'],
                             ids=['email', 'password', 'name'])
    def test_update_auth_user(self, registered_user_access_token, update_data):
        data = registered_user_access_token
        fake = Faker()
        payload = update_data
        access_token = data.json()['accessToken']
        headers = {"Authorization": f"{access_token}"}
        request_url = f'{url.BASE_URL}{ep.UPDATE_USER}'
        with allure.step("Шаг 1: Отправка PATCH-запроса на изменение {update_data} у пользователя"):
            response = requests.patch(request_url, data=payload, headers=headers)
            email = response.json()['user']['email']
            name = response.json()['user']['name']
        with allure.step("Шаг 2: Проверка кода ответа"):
            assert response.status_code == 200, "Ошибка: Неверный код ответа"
        with allure.step("Шаг 3: Проверка сообщения об успешном изменении данных пользователя"):
            assert response.text == f'{{"success":true,"user":{{"email":"{email}","name":"{name}"}}}}', "Ошибка: Неверное сообщение"


    @allure.title('Изменение данных для не авторизованного пользователя')
    @allure.description('Тест проверяет ошибку изменения поля {update_data} у неавторизованного пользователя')
    @pytest.mark.parametrize('update_data', ['{"email": fake.email(), "password": data[1],"name": data[2]}',
                                              '{"email": data[0], "password": fake.password(), "name": data[2]}',
                                              '{"email": data[0], "password":data[1], "name":fake.name()}'],
                             ids=['email', 'password', 'name'])
    def test_update_non_auth_user(self, registered_user_access_token, update_data):
        data = registered_user_access_token
        fake = Faker()
        payload = update_data
        request_url = f'{url.BASE_URL}{ep.UPDATE_USER}'
        with allure.step("Шаг 1: Отправка PATCH-запроса на изменение {update_data} у не авторизованного пользователя"):
            response = requests.patch(request_url, data=payload)
        with allure.step("Шаг 2: Проверка кода ответа"):
            assert response.status_code == 401, "Ошибка: Неверный код ответа"
        with allure.step("Шаг 3: Проверка сообщения что данные не обновлены (нет полномочий)"):
            assert response.text == '{"success":false,"message":"You should be authorised"}', "Ошибка: Неверное сообщение"