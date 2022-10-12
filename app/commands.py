import random

from fastapi import FastAPI
from fastapi import Request
from fastapi.exceptions import RequestValidationError

from app.core.utils import get_quiz, get_json_response, check_entry_in_list
from app.schemes.base_schemas import Block
from app.schemes.request_schemas import CheckAnswerRequest, ExcludeTwoAnswersRequest, GetQuestionWithAnswersRequest

fast_app = FastAPI()


@fast_app.post("/get_question_with_answers")
async def get_question_with_answers(user_request: GetQuestionWithAnswersRequest) -> None:
    pass


@fast_app.post("/check_answer_user")
async def check_answer_user(user_request: CheckAnswerRequest):
    quiz = get_quiz()

    # Валидация данных
    # Проверка верного названия блока
    try:
        level: list['Block'] = getattr(quiz, user_request.name_block)
    except AttributeError:
        return get_json_response("There is no block with this name")

    # Проверка попадания в списки
    if check_entry_in_list(user_request.number_question_in_block, level) is False:
        return get_json_response("There is no such id in the block")

    # Проверка корректности id ответа
    answer_id = user_request.answer_id
    block = level[user_request.number_question_in_block]
    if check_entry_in_list(answer_id, block.answers) is False:
        return get_json_response("Invalid response number")

    # Проверяем верность ответа
    right_answer = block.right_answer
    response = right_answer == user_request.answer_id

    return {"status": "success", "answer": response}


@fast_app.post("/exclude_two_answers")
async def exclude_two_answers(user_request: ExcludeTwoAnswersRequest):
    quiz = get_quiz()

    # Валидация данных
    # Проверка верного названия блока
    try:
        level: list['Block'] = getattr(quiz, user_request.name_block)
    except AttributeError:
        return get_json_response("There is no block with this name")

    # Проверка попадания в списки
    if check_entry_in_list(user_request.number_question_in_block, level) is False:
        return get_json_response("There is no such id in the block")

    block = level[user_request.number_question_in_block]
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
