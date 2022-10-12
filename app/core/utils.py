import json
import os.path
import random
import string
from pathlib import Path

from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from app.schemes.base_schemas import Quiz, User


def get_project_root():
    return Path(__file__).parent.parent.parent


def get_quiz() -> Quiz:
    """
        Возвращает объект quiz созданный на основе данных из quiz.json
    :return:
    """
    path_quiz = os.path.join(get_project_root(), r"static\quiz.json")
    with open(path_quiz, 'r', encoding="utf-8") as fr:
        data = json.loads(fr.read())
        return Quiz(**data)


def get_users() -> list['User']:
    """
        Возвращает список пользователей из users.json
    :return:
    """
    path_users = os.path.join(get_project_root(), r"static\users.json")
    with open(path_users, 'r', encoding="utf-8") as fr:
        data = json.loads(fr.read())
        if len(data["users"]) == 0:
            return []
        return [User(**user) for user in data["users"]]


def save_users(users: list['User']) -> None:
    path_users = os.path.join(get_project_root(), r"static\users.json")
    with open(path_users, 'w', encoding="utf-8") as fw:
        convertor = {"users": []}
        for user in users:
            convertor["users"].append(user.dict())
        ready_json = json.dumps(convertor)
        fw.write(ready_json)


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


def generate_unique_user_id() -> str:
    """
        Генерация случайного user_id
    :return:
    """
    users = get_users()
    while True:
        user_id = generate_random_string(length=25)
        duplicate_found = False
        for user in users:
            if user.user_id == user_id:
                duplicate_found = True
                break

        if duplicate_found is False:
            return user_id


def generate_random_string(length) -> str:
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string
