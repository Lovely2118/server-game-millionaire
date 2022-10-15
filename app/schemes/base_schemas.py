from pydantic import BaseModel


class Block(BaseModel):
    question: str
    answers: list['str']
    right_answer: int
    level: int
    cost: int


class Quiz(BaseModel):
    blocks: list['Block']


class User(BaseModel):
    user_id: str
    name: str | None
    money: int | float
    name_block: str
    number_question_in_block: int
