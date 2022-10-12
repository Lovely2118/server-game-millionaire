import json

from tests.test_utils import setup  # type: ignore

exclude_two_answers_correct_request = {
    "user_id": "test_user_id",
}

exclude_two_answers_without_parameters = {}


def test_exclude_two_answers_with_correct_request(setup) -> None:
    """
        Тестируем в случае если клиент отправил данные корректно
    :param setup:
    :return:
    """

    # Подготовка данных
    global exclude_two_answers_correct_request
    client = setup

    # Тестирование требуемой функции
    response_exclude_two_answers = client.post("/exclude_two_answers",
                                               data=json.dumps(exclude_two_answers_correct_request))

    # Проверка результатов
    assert response_exclude_two_answers.status_code == 200
    response_json = response_exclude_two_answers.json()
    answer = response_json["answer"]
    right_answer = response_json["answer"]["right_answer"]

    assert response_json["status"] == "success"
    assert answer["question"] == "Как называют погоду, когда температура опускается гораздо ниже нуля?"
    assert answer["answers"][right_answer] == "собачий холод"
    assert len(answer["answers"]) == 2


def test_exclude_two_answers_without_parameters(setup) -> None:
    """
        Тестируем в случае если клиент отправил пустой запрос
    :param setup:
    :return:
    """

    # Подготовка данных
    global exclude_two_answers_without_parameters
    client = setup

    # Тестирование требуемой функции
    response_exclude_two_answers = client.post("/exclude_two_answers",
                                               data=json.dumps(exclude_two_answers_without_parameters))

    # Тестирование результатов
    assert response_exclude_two_answers.status_code == 422
    assert response_exclude_two_answers.json() == {"status": "error", "answer": "Invalid data type"}
