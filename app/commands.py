import random

from fastapi import FastAPI
from fastapi import Request
from fastapi.exceptions import RequestValidationError

from app.core.utils import get_quiz, get_json_response, check_entry_in_list, get_users, generate_random_string, \
    generate_unique_user_id
from app.errors import UserIsNotInJson, UserAlreadyExists
from app.handler_users import get_user_by_id, add_user, go_to_next_question
from app.schemes.base_schemas import Block, User
from app.schemes.request_schemas import CheckAnswerRequest, ExcludeTwoAnswersRequest, GetQuestionWithAnswersRequest, \
    RegisterUserRequest

fast_app = FastAPI()


@fast_app.get("/check_user_by_name")
def check_user_by_name() -> None:
    pass


@fast_app.get("/get_money_user")
def get_money_user() -> None:
    pass


@fast_app.post("/register_user")
async def register_user(user_request: RegisterUserRequest):
    """
        Регистрация пользователя на сервере
    """
    users = get_users()

    # Валидация данных
    try:
        unique_user_id = generate_unique_user_id()
        new_user = User(user_id=unique_user_id, name=user_request.name, money=0, name_block="level_1", number_question_in_block=0)
        add_user(new_user, users)
    except UserAlreadyExists:
        # todo поменять ошибку
        return get_json_response("The user does not exist")
    return {"status": "success", "answer": {"user_id": unique_user_id}}


@fast_app.post("/get_question_with_answers")
async def get_question_with_answers(user_request: GetQuestionWithAnswersRequest):
    """
        Получить вопрос и ответы для выбранного пользователя
    """
    quiz = get_quiz()
    users = get_users()

    # Валидация данных
    # Проверка существования пользователя и верного названия блока
    try:
        selected_user = get_user_by_id(user_request.user_id, users)
        level: list['Block'] = getattr(quiz, selected_user.name_block)
    except UserIsNotInJson:
        return get_json_response("The user does not exist")
    except AttributeError:
        return get_json_response("There is no block with this name")

    block = level[selected_user.number_question_in_block]
    return {"status": "success", "answer": {"question": block.question,
                                            "answers": block.answers}}


@fast_app.post("/check_answer_user")
async def check_answer_user(user_request: CheckAnswerRequest):
    """
        Проверить вопрос пользователя на правильность
    """
    quiz = get_quiz()
    users = get_users()

    # Валидация данных
    # Проверка существования пользователя и верного названия блока
    try:
        selected_user = get_user_by_id(user_request.user_id, users)
        level: list['Block'] = getattr(quiz, selected_user.name_block)
    except UserIsNotInJson:
        return get_json_response("The user does not exist")
    except AttributeError:
        return get_json_response("There is no block with this name")

    # Проверка корректности id ответа
    answer_id = user_request.answer_id
    block = level[selected_user.number_question_in_block]
    if check_entry_in_list(answer_id, block.answers) is False:
        return get_json_response("Invalid response number")

    # Проверяем верность ответа
    right_answer = block.right_answer
    response = right_answer == user_request.answer_id
    if response:
        go_to_next_question(selected_user, level)
    return {"status": "success", "answer": response}


@fast_app.post("/exclude_two_answers")
async def exclude_two_answers(user_request: ExcludeTwoAnswersRequest):
    """
        Удалить два неверных ответа
    """
    quiz = get_quiz()
    users = get_users()

    # Валидация данных
    # Проверка существования пользователя и верного названия блока
    try:
        selected_user = get_user_by_id(user_request.user_id, users)
        level: list['Block'] = getattr(quiz, selected_user.name_block)
    except UserIsNotInJson:
        return get_json_response("The user does not exist")
    except AttributeError:
        return get_json_response("There is no block with this name")

    block = level[selected_user.number_question_in_block]
    right_answer_text = block.answers[block.right_answer]
    answer_options = [0, 1, 2, 3]
    # Удаляем правильный ответ
    answer_options.remove(block.right_answer)
    # Получаем не правильный ответ
    wrong_answer = answer_options[random.randint(0, len(answer_options) - 1)]
    return {"status": "success", "answer": {
        "question": block.question,
        "answers": [right_answer_text, wrong_answer],
        "right_answer": 0
    }}


@fast_app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return get_json_response("Invalid data type")
