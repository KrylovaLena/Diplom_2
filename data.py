

class Urls:
    BASE_URL = 'https://stellarburgers.nomoreparties.site'

class Endpoints:
    CREATE_USER = '/api/auth/register'                  # POST Создание пользователя
    LOGIN_USER = '/api/auth/login'                      # POST Логин пользователя в системе
    DELETE_USER = '/api/auth/user'                      # DELETE Удаление пользователя
    UPDATE_USER = '/api/auth/user'                      # PATCH Обновление данных пользователя
    CREATE_ORDER = '/api/orders'                        # POST Создание заказа
    GET_ORDER_LIST  = '/api/orders'                     # GET Получение списка заказов