from pydantic import BaseModel


class Block(BaseModel):
    question: str
    answers: list['str']
    right_answer: int


class Quiz(BaseModel):
    level_1: list['Block']
    level_2: list['Block']
    level_3: list['Block']
    level_4: list['Block']
    level_5: list['Block']


class User(BaseModel):
    id: str
    name: str
    money: int | float
    number_block: int
    number_question_in_block: int
