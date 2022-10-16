from pydantic import BaseModel


# todo желательно переименовать name_block в name_level или типо того


class BaseWithUserIdRequest(BaseModel):
    user_id: str


class CheckUserByUserIdRequest(BaseWithUserIdRequest):
    user_id: str | None
    name_user: str | None


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
