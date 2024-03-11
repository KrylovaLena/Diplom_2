import requests
import pytest
import allure

from data import Urls as url
from data import Endpoints as ep
import register


@pytest.fixture(scope="function")
def registered_user_access_token():
    with allure.step('Получение access_token у зарегистрированного пользователя'):
        data = register.register_new_user_and_return_name_password_email()

        yield data[1]
    with allure.step('Получение токена созданного пользователя'):
        access_token = data[1].json()["accessToken"]
    with allure.step('Удаление созданного пользователя'):
        requests.delete(f'{url.BASE_URL}{ep.DELETE_USER}', headers={'Authorization': f'{access_token}'})


@pytest.fixture(scope="function")
def register_new_user():
    with allure.step('Получение логина и пароля зарегистрированного пользователя'):
        data = register.register_new_user_and_return_name_password_email()

        yield data[0]

    with allure.step('Получение токена созданного пользователя'):
        access_token = data[1].json()["accessToken"]
    with allure.step('Удаление созданного пользователя'):
        requests.delete(f"{url.BASE_URL}{ep.DELETE_USER}", headers={'Authorization': f'{access_token}'})


@pytest.fixture(scope="function")
def ingredients():
    # Отправка GET запроса
    response = requests.get("https://stellarburgers.nomoreparties.site/api/ingredients")
    # Извлечение данных из ответа
    data = response.json()
    # Извлечение значений ключа "_id" и сохранение их в переменную "ingredients"
    ingredients = [item["_id"] for item in data["data"]]
    return ingredients


@pytest.fixture
def create_orders(registered_user_access_token, ingredients):
    data = registered_user_access_token
    access_token = data.json()['accessToken']
    headers = {"Authorization": f"{access_token}"}
    payload = {
        "ingredients": ingredients
    }
    request_url = f"{url.BASE_URL}{ep.CREATE_ORDER}"

    for _ in range(5):
        response = requests.post(request_url, json=payload, headers=headers)
        if response.status_code != 200:
            raise Exception("Неверный статус код ответа")

    return {
        "access_token": access_token
    }

