import httpx
from jsonschema import validate
from schemas.LIST_RESOURCE_SCHEMA import LIST_RESOURCE_SCHEMA
import allure

BASE_URL = "https://reqres.in"
LIST_RESOURCE = "/api/unknown"
SINGLE_RESOURCE = "/api/unknown/2"
RESOURCE_NOT_FOUND = "/api/unknown/23"


@allure.suite("Проверка cписка ресурсов")
class TestList:

    @allure.title("Проверка получения списка ресурсов")
    def test_list_resource(self):
        with allure.step(f"Делаем запрос по адресу: {BASE_URL + LIST_RESOURCE}"):
            response = httpx.get(BASE_URL + LIST_RESOURCE)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
            resource_list = response.json()['data']

        with allure.step("Проверка уникальности идентификаторов"):
            ids = [item['id'] for item in resource_list]
            assert len(ids) == len(set(ids))

        for item in resource_list:
            with allure.step("Валидация структуры элемента"):
                validate(item, LIST_RESOURCE_SCHEMA)

            for key in LIST_RESOURCE_SCHEMA['required']:
                with allure.step(f"Проверка наличия обязательного поля: {key}"):
                    assert key in item

            with allure.step("Проверка диапазона значений года"):
                assert 1900 <= item['year'] <= 2100

            with allure.step("Проверка типа идентификатора"):
                assert isinstance(item['id'], int)

            with allure.step("Проверка типа имени"):
                assert isinstance(item['name'], str)

            with allure.step("Проверка типа года"):
                assert isinstance(item['year'], int)

            with allure.step("Проверка типа цвета"):
                assert isinstance(item['color'], str)

            with allure.step("Проверка типа значения Pantone"):
                assert isinstance(item['pantone_value'], str)

    @allure.title("Проверка получения данных одного ресурса")
    def test_single_resource(self):
        with allure.step(f"Делаем запрос по адресу: {BASE_URL + SINGLE_RESOURCE}"):
            response = httpx.get(BASE_URL + SINGLE_RESOURCE)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
            response_json = response.json()

        with allure.step("Проверка наличия ключей 'data' и 'support' в ответе"):
            assert 'data' in response_json
            assert 'support' in response_json

        support_info = response_json['support']
        required_support_keys = ['url', 'text']

        for key in required_support_keys:
            with allure.step(f"Проверка наличия обязательного ключа '{key}' в информации поддержки"):
                assert key in support_info

    @allure.title("Проверка ответа для несуществующего ресурса")
    def test_resource_not_found(self):
        with allure.step(f"Делаем запрос по адресу: {BASE_URL + RESOURCE_NOT_FOUND}"):
            response = httpx.get(BASE_URL + RESOURCE_NOT_FOUND)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404
