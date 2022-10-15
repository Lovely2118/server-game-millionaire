import json
import os

from app.core.utils import get_project_root
from app.schemes.base_schemas import Quiz

__factory_quiz = None


def get_quiz() -> Quiz:
    """
        Возвращает объект quiz созданный на основе данных из quiz.json
    :return:
    """
    global __factory_quiz

    if __factory_quiz is None:
        path_quiz = os.path.join(get_project_root(), r"static\quiz.json")
        with open(path_quiz, 'r', encoding="utf-8") as fr:
            data = json.loads(fr.read())
            __factory_quiz = Quiz(**data)
    return __factory_quiz
