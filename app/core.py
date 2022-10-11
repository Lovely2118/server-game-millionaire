import json
import os.path
from pathlib import Path

from app.schemes.quiz import Quiz


def get_project_root():
    return Path(__file__).parent.parent


def get_quiz() -> Quiz:
    path_quiz = os.path.join(get_project_root(), "static\quiz.json")
    with open(path_quiz, 'r', encoding="utf-8") as fr:
        data = json.loads(fr.read())
        return Quiz(**data)
