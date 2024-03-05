Тестирование API для веб-сайта: https://stellarburgers.nomoreparties.site

Документация: https://code.s3.yandex.net/qa-automation-engineer/python-full/diploma/api-documentation.pdf?etag=3403196b527ca03259bfd0cb41163a89


Основа для написания автотестов — фреймворк pytest

Установить зависимости из requirements.txt

Команда для запуска — pytest .\tests --alluredir=allure_results


Файлы с тестами лежат в папке tests и имеют следующие название:

1. test_create_order.py - тесты по созданию заказа

test_create_order_auth_user - проверяет успешное создание заказа авторизованным пользователем с валидным хеш ингредиента;
test_create_order_non_auth_user- проверяет успешное создание заказа не авторизованным пользователем с валидным хеш ингредиента;
test_create_order_auth_user_non_ingredients- проверяет создание заказа без ингридиентов авторизованным пользователем;
test_create_order_non_auth_user_non_ingredients- проверяет создание заказа не авторизованным пользователем без ингридиентов;
test_create_order_auth_user_ingredients_false - проверяет создание заказа авторизованным пользователем при указании невалидного хеша;
test_create_order_non_auth_user_ingredients_false - проверяет создание заказа не авторизованным пользователем с невалидным хешем ингридиента.

2. test_create_user.py - тесты по регистрации нового пользователя

test_create_unique_user - проверка создания пользователя с валидными данными;
test_create_existing_user - проверка что невозможно создать пользователя который уже зарегистрирован;
test_register_new_user_without_required_field - проверяет регистрацию пользователя с пустым обязательным полем {deleted_field}.

3. test_get_order.py - тесты на получение списка заказов пользователя

test_get_orders_auth_user - проверяет последние заказы авторизованного пользователя и возвращает максимум 50 последних заказов;
test_get_orders_non_auth_user - проверяет возможность получения заказов неавторизированным пользователем.

4. test_login_user.py - тесты по авторизации пользователей

test_login_user -на возврат списка заказов в тело ответа и код ответа.проверяет успешную авторизацию зарегистрированного пользователя;
test_login_user_without_required_field - проверяет авторизацию пользователя с пустым обязательным полем {deleted_field};
test_login_user_without_password - проверяет авторизацию пользователя с неправильно заполненным password;
test_login_user_without_email - проверяет авторизацию пользователя с неправильно заполненным email.

5. test_update_user - тесты по изменению данных пользователя

test_update_auth_user - проверяет изменение поля {update_data} у авторизованного пользователя;
test_update_non_auth_user - проверяет ошибку изменения поля {update_data} у неавторизованного пользователя.