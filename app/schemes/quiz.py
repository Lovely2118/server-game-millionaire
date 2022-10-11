from pydantic import BaseModel


class Block(BaseModel):
    question: str
    answer_1: str
    answer_2: str
    answer_3: str
    answer_4: str
    right_answer: int


class Quiz(BaseModel):
    level_1: list['Block']
    level_2: list['Block']
    level_3: list['Block']
    level_4: list['Block']
    level_5: list['Block']