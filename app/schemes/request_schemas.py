from pydantic import BaseModel


# todo желательно переименовать name_block в name_level или типо того

class GetQuestionWithAnswersRequest(BaseModel):
    user_id: str


class CheckAnswerRequest(BaseModel):
    user_id: str
    answer_id: int


class ExcludeTwoAnswersRequest(BaseModel):
    user_id: str
