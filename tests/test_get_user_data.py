from http.client import responses

import httpx
from jsonschema import validate
from schemas.USER_DATA_SCHEMA import USER_DATA_SCHEMA
import allure

BASE_URL = "https://reqres.in"
LIST_USERS = "/api/users?page=2"
SINGLE_USER = "/api/users/2"
USER_NOT_FOUND = "/api/users/23"
EMAIL_ENDS = "@reqres.in"
AVATAR_ENDS = "-image.jpg"
DELAYED_REQUEST = "/api/users?delay=3"


@allure.suite("Проверка запросов данных пользователей")
class TestUserData:

    @allure.title("Проверка получения списка пользователей")
    def test_list_users(self):
        with allure.step(f"Делаем запрос по адресу: {BASE_URL + LIST_USERS}"):
            response = httpx.get(BASE_URL + LIST_USERS)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200

        data = response.json()['data']
        for item in data:
            with allure.step("Проверка элемента из списка"):
                validate(item, USER_DATA_SCHEMA)
                with allure.step("Проверка окончания Email адреса"):
                    assert item['email'].endswith(EMAIL_ENDS)

                with allure.step("Проверка наличия id в ссылке на аватарку"):
                    assert item['avatar'].endswith(str(item['id']) + AVATAR_ENDS)

    @allure.title("Проверка получения одного пользователя")
    def test_single_user(self):
        with allure.step(f"Делаем запрос по адресу: {BASE_URL + SINGLE_USER}"):
            response = httpx.get(BASE_URL + SINGLE_USER)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
            data = response.json()['data']

        with allure.step("Проверка окончания Email адреса"):
            assert data['email'].endswith(EMAIL_ENDS)

        with allure.step("Проверка формата URL аватара "):
            assert data['avatar'].endswith(str(data['id']) + AVATAR_ENDS)

    @allure.title("Проверка ответа для несуществующего пользователя")
    def test_user_not_found(self):
        with allure.step(f"Делаем запрос по адресу: {BASE_URL + USER_NOT_FOUND}"):
            response = httpx.get(BASE_URL + USER_NOT_FOUND)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404

    @allure.title("Проверка получения списка отложенных пользователей")
    def test_delayed_user_list(self):
        with allure.step(f"Делаем запрос по адресу: {BASE_URL + DELAYED_REQUEST}"):
            response = httpx.get(BASE_URL + DELAYED_REQUEST, timeout=4)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200