from app import fast_app
from app.schemes.request_schemas import UserResponse


@fast_app.post("/check_answer_user")
async def check_answer_user(user_response: UserResponse):
    pass