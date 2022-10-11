from fastapi import FastAPI
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core import get_quiz
from app.schemes.quiz import Block
from app.schemes.request_schemas import UserResponse

fast_app = FastAPI()


@fast_app.post("/check_answer_user")
async def check_answer_user(user_response: UserResponse):
    print(f"My User response: {user_response}")
    quiz = get_quiz()

    # Валидация данных
    # Проверка попадания в списки
    try:
        level: list['Block'] = getattr(quiz, user_response.name_block)
    except AttributeError:
        return {"status": "error", "answer": "There is no block with this name"}
    if (0 <= user_response.number_question_in_block < len(level)) is False:
        return {"status": "error", "answer": "There is no such id in the block"}

    # Проверка корректности id ответа
    answer_id = user_response.answer_id
    if (0 <= answer_id < 4) is False:
        return {"status": "error", "answer": "Invalid response number"}

    block = level[user_response.number_question_in_block]
    right_answer = block.right_answer
    response = right_answer == user_response.answer_id

    return {"status": "success", "answer": response}


@fast_app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"status": "error",
                                  "answer": "Invalid data type"}),
    )
