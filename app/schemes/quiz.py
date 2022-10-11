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