import json

from tests.test_utils import setup  # type: ignore

get_question_with_answers_correct_request = {
    "user_id": "test_user_id"
}

get_question_with_answers_invalid_user_id = {
    "user_id": "invalid_user_id"
}

get_question_with_answers_invalid_key_data_type = {
    "user_id": 1232141
}


def test_get_question_with_answers_correct_request(setup) -> None:
    """
        Тестирование получения вопроса и ответов для заданного пользователя
    :param setup:
    :return:
    """
    # Подготовка данных
    global get_question_with_answers_correct_request
    client = setup

    # Тестирование требуемой функции
    response_get_question_with_answers = client.post("/get_question_with_answers",
                                                     data=json.dumps(get_question_with_answers_correct_request))

    # Проверка результатов
    response_json = response_get_question_with_answers.json()
    assert response_get_question_with_answers.status_code == 200
    assert response_json["status"] == "success"
    assert "question" in response_json["answer"].keys()
    assert "answers" in response_json["answer"].keys()


def test_get_question_with_answers_invalid_user_id(setup) -> None:
    """
        Тестирование получения вопроса и ответов с пользователем которого нет в бд
    :param setup:
    :return:
    """
    # Подготовка данных
    global get_question_with_answers_invalid_user_id
    client = setup

    # Тестирование требуемой функции
    response_get_question_with_answers = client.post("/get_question_with_answers",
                                                     data=json.dumps(get_question_with_answers_invalid_user_id))

    # Проверка результатов
    assert response_get_question_with_answers.status_code == 422
    assert response_get_question_with_answers.json() == {"status": "error", "answer": "The user does not exist"}


def test_get_question_with_answers_invalid_key_data_type(setup) -> None:
    """
        Тестирование получения вопроса и ответов с неверным типом ключа пользователя
    :param setup:
    :return:
    """

    # Подготовка данных
    global get_question_with_answers_invalid_key_data_type
    client = setup

    # Тестирование требуемой функции
    response_get_question_with_answers = client.post("/get_question_with_answers",
                                                     data=json.dumps(get_question_with_answers_invalid_key_data_type))

    # Проверка результатов
    assert response_get_question_with_answers.status_code == 422
    assert response_get_question_with_answers.json() == {"status": "error", "answer": "The user does not exist"}

