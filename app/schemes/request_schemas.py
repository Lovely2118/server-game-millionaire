from pydantic import BaseModel


# todo желательно переименовать name_block в name_level или типо того


class BaseWithUserIdRequest(BaseModel):
    user_id: str


class CheckUserByUserIdRequest(BaseWithUserIdRequest):
    pass


class GetMoneyUserRequest(BaseWithUserIdRequest):
    pass


class RegisterUserRequest(BaseModel):
    name: str | None


class GetQuestionWithAnswersRequest(BaseWithUserIdRequest):
    pass


class CheckAnswerRequest(BaseWithUserIdRequest):
    answer_id: int


class ExcludeTwoAnswersRequest(BaseWithUserIdRequest):
    pass
