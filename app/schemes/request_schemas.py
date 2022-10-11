from pydantic import BaseModel


class UserResponse(BaseModel):
    user_id: str
    name_block: str
    number_question_in_block: int
    answer_user: int
