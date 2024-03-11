import allure
import pytest
import requests

from data import Urls as url
from data import Endpoints as ep


@allure.suite('Получение списка заказов пользователя')
class TestGetUserOrders:

    @allure.title('Получение списка заказов авторизованного пользователя')
    @allure.description('Тест проверяет последние заказы авторизованного пользователя и возвращает максимум 50 последних заказов')
    def test_get_orders_auth_user(self, create_orders):
        access_token = create_orders['access_token']
        headers = {"Authorization": f"{access_token}"}
        request_url = f'{url.BASE_URL}{ep.GET_ORDER_LIST}'
        with allure.step("Шаг 1: Отправка GET-запроса на получение заказов пользователя"):
            response = requests.get(request_url, headers=headers)
            json_data = response.json()
            expected_orders = response.json()['orders']
            expected_total = response.json()['total']
            expected_total_today = response.json()['totalToday']
        with allure.step("Шаг 2: Проверка кода ответа"):
            assert response.status_code == 200, "Ошибка: Неверный код ответа"
        with allure.step("Шаг 3: Проверка сообщения"):
            assert json_data["success"] is True, "Ошибка: Неверное сообщение"
        with allure.step("Шаг 4: Проверка заказов и общей информации"):
            assert json_data["orders"] == expected_orders, "Ошибка: Неверный список заказов"
            assert json_data["total"] == expected_total, "Ошибка: Неверное общее количество заказов"
            assert json_data["totalToday"] == expected_total_today, "Ошибка: Неверное общее количество заказов за сегодня"


    @allure.title('Получение списка заказов неавторизированного пользователя')
    @allure.description('Тест проверяет возможность получения заказов неавторизированным пользователем')
    def test_get_orders_non_auth_user(self):
        with allure.step("Шаг 1: Отправка GET-запроса на получение заказов неавторизованного пользователя"):
            request_url = f"{url.BASE_URL}{ep.CREATE_ORDER}"
            response = requests.get(request_url)
        with allure.step("Шаг 2: Проверка кода ответа"):
            assert response.status_code == 401, "Ошибка: Неверный код ответа"
        with allure.step("Шаг 3: Проверка сообщения об ошибке"):
            assert response.text == '{"success":false,"message":"You should be authorised"}', "Ошибка: Неверное сообщение"