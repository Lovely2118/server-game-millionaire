import json

from tests.test_utils import setup, teardown  # type: ignore

get_user_registration_is_valid_request = {
    "user_id": None,
    "name_user": "test_name"
}

get_user_valid_request = {
    "user_id": "test_user_id",
    "name_user": None
}

get_user_valid_with_incorrect_name_request = {
    "user_id": "test_user_id",
    "name_user": "test_incorrect_name"
}

get_user_with_incorrect_data = {
    "user_id": None,
    "name_user": None
}


def test_get_user_registration_is_valid_request(setup) -> None:
    """
        Тестирование регистрации пользователя с вводом имени
    """
    # Подготовка данных
    global get_user_registration_is_valid_request
    client, user_id = setup["fast_api_client"], setup["user_id"]

    # Вызов тестируемой функции
    response_get_user = client.post("/get_user", data=json.dumps(get_user_registration_is_valid_request))

    # Тестирование результатов
    answer_json = response_get_user.json()

    assert response_get_user.status_code == 200
    assert answer_json["status"] == "success"
    assert answer_json["answer"]["user_found"] is False
    assert answer_json["answer"]["name"] == "test_name"
    assert answer_json["answer"]["money"] == 100


def test_get_user_valid_request(setup) -> None:
    """
        Тестирование получения пользователя по user_id
    """
    # Подготовка данных
    global get_user_valid_request
    client, user_id = setup["fast_api_client"], setup["user_id"]

    # Вызов тестируемой функции
    response_get_user = client.post("/get_user", data=json.dumps(get_user_valid_request))

    # Тестирование результатов
    answer_json = response_get_user.json()

    assert response_get_user.status_code == 200
    assert answer_json["status"] == "success"
    assert answer_json["answer"]["user_found"] is True
    assert answer_json["answer"]["user_id"] == "test_user_id"
    assert answer_json["answer"]["name"] == "test_name"
    assert answer_json["answer"]["money"] == 100


def test_get_user_valid_with_incorrect_name_request(setup) -> None:
    """
        Тестирование получения пользователя по имени и по user_id
    """
    # Подготовка данных
    global get_user_valid_with_incorrect_name_request
    client, user_id = setup["fast_api_client"], setup["user_id"]

    # Вызов тестируемой функции
    response_get_user = client.post("/get_user", data=json.dumps(get_user_valid_with_incorrect_name_request))

    # Тестирование результатов
    answer_json = response_get_user.json()

    assert response_get_user.status_code == 200
    assert answer_json["status"] == "success"
    assert answer_json["answer"]["user_found"] is True
    assert answer_json["answer"]["name"] == "test_name"
    assert answer_json["answer"]["money"] == 100


def test_get_user_with_incorrect_data(setup) -> None:
    """
        Тестирование получения пользователя без ввода имени и user_id
    """
    global get_user_with_incorrect_data
    client, user_id = setup["fast_api_client"], setup["user_id"]

    # Вызов тестируемой функции
    response_get_user = client.post("/get_user", data=json.dumps(get_user_with_incorrect_data))

    # Тестирование результатов
    assert response_get_user.status_code == 422
    assert response_get_user.json() == {"status": "error", "answer": "Invalid data type"}