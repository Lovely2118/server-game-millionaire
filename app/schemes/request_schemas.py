from pydantic import BaseModel


class CheckAnswerResponse(BaseModel):
    user_id: str
    name_block: str
    number_question_in_block: int
    answer_id: int


class ExcludeTwoAnswersResponse(BaseModel):
    user_id: str
    name_block: str
    number_question_in_block: int
