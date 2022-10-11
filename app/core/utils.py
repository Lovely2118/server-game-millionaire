import json
import os.path
from pathlib import Path

from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from app.schemes.quiz import Quiz


def get_project_root():
    return Path(__file__).parent.parent.parent


def get_quiz() -> Quiz:
    path_quiz = os.path.join(get_project_root(), "static\quiz.json")
    with open(path_quiz, 'r', encoding="utf-8") as fr:
        data = json.loads(fr.read())
        return Quiz(**data)


def check_entry_in_list(index: int, selected_list: list) -> bool:
    """
        Проверяем чтобы элемент входил в список
    :param index:
    :param selected_list:
    :return:
    """
    return 0 <= index < len(selected_list)


def get_json_response(answer: str) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"status": "error",
                                  "answer": answer}),
    )
