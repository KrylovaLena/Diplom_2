import string
import random
import requests
import uuid

# если регистрация не удалась, возвращает пустой список
def register_new_user_and_return_name_password_email():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # создаём список, чтобы метод мог его вернуть
    login_pass = []

    # генерируем email, login и password
    name = generate_random_string(10)
    password = generate_random_string(10)
    email = str(uuid.uuid4())[:8] + "@example.com"
    # собираем тело запроса
    payload = {
        "email": email,
        "password": password,
        "name": name

    }
    # отправляем запрос на регистрацию пользователя и сохраняем ответ в переменную response
    response = requests.post('https://stellarburgers.nomoreparties.site/api/auth/register', data=payload)
    # если регистрация прошла успешно (код ответа 200), добавляем в список email, имя и пароль пользователя
    if response.status_code == 200:
        login_pass.append(email)
        login_pass.append(password)
        login_pass.append(name)

    # возвращаем список
    return login_pass, response