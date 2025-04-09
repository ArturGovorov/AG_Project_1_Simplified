import httpx
from jsonschema import validate

from core.contracts import USER_DATA_SCHEMA
from core.contracts import LIST_RESOURCE_SCHEMA

BASE_URL = "https://reqres.in"
LIST_USERS = "/api/users?page=2"
SINGLE_USER = "/api/users/2"
USER_NOT_FOUND = "/api/users/23"
EMAIL_ENDS = "@reqres.in"
AVATAR_ENDS = "-image.jpg"
LIST_RESOURCE = "/api/unknown"
SINGLE_RESOURCE = "/api/unknown/2"
RESOURCE_NOT_FOUND = "/api/unknown/23"


def test_list_users():
    response = httpx.get(BASE_URL + LIST_USERS)
    assert response.status_code == 200
    data = response.json()['data']

    for item in data:
        validate(item, USER_DATA_SCHEMA)
        assert item['email'].endswith(EMAIL_ENDS)
        # assert str(item['id']) in item ['avatar']
        assert item['avatar'].endswith(str(item['id']) + AVATAR_ENDS)


def test_single_user():
    response = httpx.get(BASE_URL + SINGLE_USER)
    assert response.status_code == 200
    data = response.json()['data']
    assert data['email'].endswith(EMAIL_ENDS)
    assert data['avatar'].endswith(str(data['id']) + AVATAR_ENDS)


def test_user_not_found():
    response = httpx.get(BASE_URL + USER_NOT_FOUND)
    assert response.status_code == 404


def test_list_resource():
    response = httpx.get(BASE_URL + LIST_RESOURCE)
    assert response.status_code == 200
    resource_list = response.json()['data']
    ids = [item['id'] for item in resource_list]
    assert len(ids) == len(set(ids))

    for item in resource_list:
        validate(item, LIST_RESOURCE_SCHEMA)
        for key in LIST_RESOURCE_SCHEMA['required']:
            assert key in item
        assert 1900 <= item['year'] <= 2100
        assert isinstance(item['id'], int)
        assert isinstance(item['name'], str)
        assert isinstance(item['year'], int)
        assert isinstance(item['color'], str)
        assert isinstance(item['pantone_value'], str)


def test_single_resource():
    response = httpx.get(BASE_URL + SINGLE_RESOURCE)
    assert response.status_code == 200
    response_json = response.json()
    assert 'data' in response_json
    assert 'support' in response_json
    support_info = response_json['support']
    required_support_keys = ['url', 'text']
    for key in required_support_keys:
        assert key in support_info


def test_resource_not_found():
    response = httpx.get(BASE_URL + RESOURCE_NOT_FOUND)
    assert response.status_code == 404
