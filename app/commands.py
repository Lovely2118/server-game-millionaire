import random

from fastapi import FastAPI
from fastapi import Request
from fastapi.exceptions import RequestValidationError

from app.core.database_utils import generate_unique_user_id, get_user_by_user_id
from app.core.utils import get_json_response, check_entry_in_list
from app.errors import UserIsNotInDatabase, UserAlreadyExists
from app.models.quiz_models import BlockModel, AnswerModel
from app.schemes.base_schemas import Block, User
from app.schemes.request_schemas import CheckAnswerRequest, ExcludeTwoAnswersRequest, GetQuestionWithAnswersRequest, \
    RegisterUserRequest, CheckUserByUserIdRequest, GetMoneyUserRequest

fast_app = FastAPI()


@fast_app.post("/get_user")
def get_user_by_user_id(user_request: CheckUserByUserIdRequest):
    """
        Возвращает true/false в зависимости от того есть такой пользователь в системе или нет
        Для работы требуется user_id
    :return:
    """
    return {"status": "success", "answer": {
        "user_found": True,  # Если пользователь в системе есть, иначе False
        "user_id": "id пользователя",  # Думаю сделать чтобы пользователю не нужно будет регистрироваться,
        # Если в запрос будет передано только имя, метод будет его регистрировать
        "name": "Имя пользователя",  # Имя пользователя в игре
        "money": "Кол-во монет пользователя"  # Кол-во монет которые есть у пользователя
    }}


@fast_app.post("/get_money_user")
def get_money_user(user_request: GetMoneyUserRequest):
    """
        Возвращает кол-во монет пользователя, если пользователь есть
    :return:
    """
    return {"status": "success", "answer": {
        "money": 0  # кол-во монет пользователя
    }}


# @fast_app.post("/register_user")
# async def register_user(user_request: RegisterUserRequest):
#     """
#         Регистрация пользователя, если до этого его не было
#     """
#     # users = get_users()
#
#     # Валидация данных
#     try:
#         unique_user_id = generate_unique_user_id()
#         new_user = User(user_id=unique_user_id, name=user_request.name, money=0, name_block="level_1",
#                         number_question_in_block=0)
#         add_user(new_user, users)
#     except UserAlreadyExists:
#         # todo поменять ошибку
#         return get_json_response("The user does not exist")
#     return {"status": "success", "answer": {"user_id": unique_user_id}}


@fast_app.post("/get_question_with_answers")
async def get_question_with_answers(user_request: GetQuestionWithAnswersRequest):
    """
        Получить вопрос и ответы для выбранного пользователя
        Так же возвращает информацию о том является бло последним для ответа
    """
    # Валидация данных
    # Проверка существования пользователя и верного названия блока
    try:
        selected_user = get_user_by_user_id(user_request.user_id)
        block: BlockModel = selected_user.block
    except UserIsNotInDatabase:
        return get_json_response("The user does not exist")
    except AttributeError:
        return get_json_response("There is no block with this name")

    return {"status": "success", "answer": {"question": block.question,
                                            "answers": block.answers}}


@fast_app.post("/check_answer_user")
async def check_answer_user(user_request: CheckAnswerRequest):
    """
        Проверить ответ пользователя на правильность
        Если ответ правильный, сервер сам переключит вопрос и ответы на следующий
    """
    # quiz = get_quiz()
    # users = get_users()

    # Валидация данных
    # Проверка существования пользователя и верного названия блока
    try:
        selected_user = get_user_by_user_id(user_request.user_id)
        block: BlockModel = selected_user.block
    except UserIsNotInDatabase:
        return get_json_response("The user does not exist")
    except AttributeError:
        return get_json_response("There is no block with this name")

    # Проверка корректности id ответа
    answer_id = user_request.answer_id
    if check_entry_in_list(answer_id, block.answers) is False:
        return get_json_response("Invalid response number")

    # Проверяем верность ответа
    right_answer = block.right_answer
    response = right_answer == user_request.answer_id
    # if response:
    #     go_to_next_question(selected_user, level)
    return {"status": "success", "answer": response}


@fast_app.post("/exclude_two_answers")
async def exclude_two_answers(user_request: ExcludeTwoAnswersRequest):
    """
        Вырезает два неверных ответа у пользователя
    """
    # quiz = get_quiz()
    # users = get_users()

    # Валидация данных
    # Проверка существования пользователя и верного названия блока
    try:
        selected_user = get_user_by_user_id(user_request.user_id)
        block: BlockModel = selected_user.block
        answers: list['AnswerModel'] = block.answers[::-1]
    except UserIsNotInDatabase:
        return get_json_response("The user does not exist")
    except AttributeError:
        return get_json_response("There is no block with this name")
    right_answer_text = answers[block.right_answer].answer
    answer_options = [0, 1, 2, 3]
    # Удаляем правильный ответ
    answer_options.remove(block.right_answer)
    # Получаем не правильный ответ
    wrong_answer = block.answers[random.randint(0, len(answer_options) - 1)].answer
    return {"status": "success", "answer": {
        "question": block.question,
        "answers": [right_answer_text, wrong_answer],
        "right_answer": 0
    }}


@fast_app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return get_json_response("Invalid data type")
