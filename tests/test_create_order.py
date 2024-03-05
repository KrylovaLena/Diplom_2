import allure
import pytest
import requests

from data import Urls as url
from data import Endpoints as ep

@allure.suite('Создание заказа')
class TestCreateOrder:
    @allure.title("Создание заказа авторизованным пользователем")
    @allure.description("Тест проверяет успешное создание заказа авторизованным пользователем с валидным хеш ингредиента")
    def test_create_order_auth_user(self, registered_user_access_token, ingredients):
        data = registered_user_access_token
        access_token = data.json()['accessToken']
        headers = {"Authorization": f"{access_token}"}
        payload = {
            "ingredients": ingredients
        }
        request_url = f'{url.BASE_URL}{ep.CREATE_ORDER}'
        with allure.step("Шаг 1: Отправка POST-запроса на создание заказа"):
            response = requests.post(request_url, data=payload, headers=headers)
        with allure.step("Шаг 2: Проверка кода ответа"):
            assert response.status_code == 200, "Ошибка: Неверный код ответа"

    @allure.title("Создание заказа не авторизованным пользователем")
    @allure.description("Тест проверяет успешное создание заказа не авторизованным пользователем с валидным хеш ингредиента")
    def test_create_order_non_auth_user(self, ingredients):
        payload = {
            "ingredients": ingredients
        }
        request_url = f'{url.BASE_URL}{ep.CREATE_ORDER}'
        with allure.step("Шаг 1: Отправка POST-запроса на создание заказа"):
            response = requests.post(request_url, data=payload)
            name = response.json()['name']
            order_number = response.json()["order"]["number"]
        with allure.step("Шаг 2: Проверка кода ответа"):
            assert response.status_code == 200, "Ошибка: Неверный код ответа"
        with allure.step("Шаг 3: Проверка сообщения об успешном создании заказа (с номером заказа)"):
            assert response.text == f'{{"success":true,"name":"{name}","order":{{"number":{order_number}}}}}'

    @allure.title("Создание заказа без ингридиентов авторизованным пользователем")
    @allure.description(
        "Тест проверяет создание заказа без ингридиентов авторизованным пользователем")
    def test_create_order_auth_user_non_ingredients(self, registered_user_access_token):
        data = registered_user_access_token
        access_token = data.json()['accessToken']
        headers = {"Authorization": f"{access_token}"}
        payload = {
            "ingredients": ""
        }
        request_url = f'{url.BASE_URL}{ep.CREATE_ORDER}'
        with allure.step("Шаг 1: Отправка POST-запроса на создание заказа"):
            response = requests.post(request_url, data=payload, headers=headers)
        with allure.step("Шаг 2: Проверка кода ответа"):
            assert response.status_code == 400, "Ошибка: Неверный код ответа"
        with allure.step("Шаг 3: Проверка сообщения об неуспешном создании заказа (так как нет ингридиентов)"):
            assert response.text == '{"success":false,"message":"Ingredient ids must be provided"}'

    @allure.title("Создание заказа не авторизованным пользователем без ингридиентов")
    @allure.description(
        "Тест проверяет создание заказа не авторизованным пользователем без ингридиентов")
    def test_create_order_non_auth_user_non_ingredients(self):
        payload = {
            "ingredients": ""
        }
        request_url = f'{url.BASE_URL}{ep.CREATE_ORDER}'
        with allure.step("Шаг 1: Отправка POST-запроса на создание заказа"):
            response = requests.post(request_url, data=payload)
        with allure.step("Шаг 2: Проверка кода ответа"):
            assert response.status_code == 400, "Ошибка: Неверный код ответа"
        with allure.step("Шаг 3: Проверка сообщения об ytуспешном создании заказа"):
            assert response.text == '{"success":false,"message":"Ingredient ids must be provided"}'

    @allure.title("Создание заказа авторизованным пользователем с невалидным хеш ингредиента")
    @allure.description(
        "Тест проверяет создание заказа авторизованным пользователем при указании невалидного хеша")
    def test_create_order_auth_user_ingredients_false(self, registered_user_access_token):
        data = registered_user_access_token
        access_token = data.json()['accessToken']
        headers = {"Authorization": f"{access_token}"}
        payload = {
            "ingredients": "ЕЕЕ111"
        }
        request_url = f'{url.BASE_URL}{ep.CREATE_ORDER}'
        with allure.step("Шаг 1: Отправка POST-запроса на создание заказа"):
            response = requests.post(request_url, data=payload, headers=headers)
        with allure.step("Шаг 2: Проверка кода ответа"):
            assert response.status_code == 500, "Ошибка: Неверный код ответа"

    @allure.title("Создание заказа не авторизованным пользователем с невалидным хешем ингридиента")
    @allure.description(
        "Тест проверяет создание заказа не авторизованным пользователем с невалидным хешем ингридиента")
    def test_create_order_non_auth_user_ingredients_false(self):
        payload = {
            "ingredients": "ЕЕЕ111"
        }
        request_url = f'{url.BASE_URL}{ep.CREATE_ORDER}'
        with allure.step("Шаг 1: Отправка POST-запроса на создание заказа"):
            response = requests.post(request_url, data=payload)
        with allure.step("Шаг 2: Проверка кода ответа"):
            assert response.status_code == 500, "Ошибка: Неверный код ответа"
