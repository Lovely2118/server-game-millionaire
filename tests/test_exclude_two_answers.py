import json

from tests.test_utils import setup  # type: ignore

exclude_two_answers_correct_request = {
    "user_id": "test_user_id",
    "name_block": "level_1",
    "number_question_in_block": 1
}

exclude_two_answers_with_invalid_block_name = {
    "user_id": "test_user_id",
    "name_block": "level_45",
    "number_question_in_block": 1
}

exclude_two_answers_without_parameters = {}


exclude_two_answers_with_incorrect_question_number_in_block = {
    "user_id": "test_user_id",
    "name_block": "level_45",
    "number_question_in_block": -123
}


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

    # Тестирование результатов
    assert response_exclude_two_answers.status_code == 200
    response_json = response_exclude_two_answers.json()
    answer = response_json["answer"]
    right_answer = response_json["answer"]["right_answer"]

    assert response_json["status"] == "success"
    assert answer["question"] == "Кем была девочка, которая несла бабушке пирожки в сказке «Красная шапочка»?"
    assert answer["answers"][right_answer] == "внучкой бабушки"
    assert len(answer["answers"]) == 2


def test_exclude_two_answers_with_invalid_block_name(setup) -> None:
    """
        Тестируем в случае если клиент отправил с неверным названием блока
    :param setup:
    :return:
    """

    # Подготовка данных
    global exclude_two_answers_with_invalid_block_name
    client = setup

    # Тестирование требуемой функции
    response_exclude_two_answers = client.post("/exclude_two_answers",
                                               data=json.dumps(exclude_two_answers_with_invalid_block_name))

    # Тестирование результатов
    assert response_exclude_two_answers.status_code == 422
    assert response_exclude_two_answers.json() == {"status": "error", "answer": "There is no block with this name"}


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


def test_exclude_two_answers_with_incorrect_question_number_in_block(setup) -> None:
    """
        Тестируем в случае если клиент отправил с неверным номером(id) вопроса и ответов
    :param setup:
    :return:
    """

    # Подготовка данных
    global exclude_two_answers_with_incorrect_question_number_in_block
    client = setup

    # Тестирование требуемой функции
    response_exclude_two_answers = client.post("/exclude_two_answers",
                                               data=json.dumps(exclude_two_answers_with_incorrect_question_number_in_block))

    # Тестирование результатов
    assert response_exclude_two_answers.status_code == 422
    assert response_exclude_two_answers.json() == {"status": "error", "answer": "There is no such id in the block"}
