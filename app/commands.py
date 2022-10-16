import random

from fastapi import FastAPI
from fastapi import Request
from fastapi.exceptions import RequestValidationError

from app.core.databasemanager import DatabaseManager
from app.core.utils import get_json_response, check_entry_in_list
from app.errors import UserIsNotInDatabase, MyException
from app.models.quiz_models import BlockModel, AnswerModel
from app.schemes.request_schemas import CheckAnswerRequest, ExcludeTwoAnswersRequest, GetQuestionWithAnswersRequest, \
    GetUserRequest

fast_app = FastAPI()


@fast_app.post("/get_data_about_user")
def get_data_about_user(user_request: GetUserRequest):
    """
        Возвращает true/false в зависимости от того есть такой пользователь в системе или нет
        Также возвращает доп. информацию о пользователе
        Для работы требуется user_id
    :return:
    """
    # Валидация данных
    db_manager = DatabaseManager()
    if user_request.user_id is not None:
        # Пытаемся получить пользователя по user_id
        try:
            selected_user = db_manager.get_user_by_user_id(user_request.user_id)
            user_found = True
        except UserIsNotInDatabase:
            return get_json_response("The user does not exist")

    elif user_request.name_user is not None:
        # Пытаемся зарегистрировать пользователя
        try:
            selected_user = db_manager.register_user(user_request.name_user)
            user_found = False
        except MyException as e:
            return get_json_response(str(e))

    else:
        # В случае если не передан user_id и name_user
        return get_json_response("Invalid data type")

    return {"status": "success", "answer": {
        "user_found": user_found,
        "user_id": selected_user.user_id,
        "name": selected_user.name,
        "money": selected_user.money
    }}


@fast_app.post("/get_question_with_answers")
async def get_question_with_answers(user_request: GetQuestionWithAnswersRequest):
    """
        Получить вопрос и ответы для выбранного пользователя
        Так же возвращает информацию о том является бло последним для ответа
    """
    # Валидация данных
    db_manager = DatabaseManager()
    try:
        # Проверка существования пользователя и верного названия блока
        selected_user = db_manager.get_user_by_user_id(user_request.user_id)
        block: BlockModel = selected_user.blocks[selected_user.number_block]
    except UserIsNotInDatabase:
        return get_json_response("The user does not exist")

    return {"status": "success", "answer": {"question": block.question,
                                            "answers": block.answers}}


@fast_app.post("/check_answer_user")
async def check_answer_user(user_request: CheckAnswerRequest):
    """
        Проверить ответ пользователя на правильность
        Если ответ правильный, сервер сам переключит вопрос и ответы на следующий
    """
    # Валидация данных
    db_manager = DatabaseManager()
    try:
        # Проверка существования пользователя и верного названия блока
        selected_user = db_manager.get_user_by_user_id(user_request.user_id)
        block: BlockModel = selected_user.blocks[selected_user.number_block]
    except UserIsNotInDatabase:
        return get_json_response("The user does not exist")

    # Проверка корректности id ответа
    answer_id = user_request.answer_id
    if check_entry_in_list(answer_id, block.answers) is False:
        return get_json_response("Invalid response number")

    # Проверяем верность ответа
    right_answer = block.right_answer
    response = right_answer == user_request.answer_id
    return {"status": "success", "answer": response}


@fast_app.post("/exclude_two_answers")
async def exclude_two_answers(user_request: ExcludeTwoAnswersRequest):
    """
        Вырезает два неверных ответа у пользователя
    """
    # Валидация данных
    db_manager = DatabaseManager()
    try:
        # Проверка существования пользователя и верного названия блока
        selected_user = db_manager.get_user_by_user_id(user_request.user_id)
        block: BlockModel = selected_user.blocks[selected_user.number_block]
        answers: list['AnswerModel'] = block.answers
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
