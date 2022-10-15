import random
import string
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.errors import UserIsNotInDatabase
from app.models.quiz_models import UserModel


def get_user_by_user_id(user_id: str) -> UserModel:
    with SessionLocal() as session:
        user = __get_user_by_user_id(session, user_id)
        if user is None:
            raise UserIsNotInDatabase()
        return user


def __get_user_by_user_id(session: Session, user_id: str) -> UserModel | None:
    user = session.query(UserModel).filter(UserModel.user_id == user_id).first()
    return user


def check_user_by_user_id(user_id: str) -> bool:
    with SessionLocal() as session:
        user = __get_user_by_user_id(session, user_id)
        return user is not None





def generate_unique_user_id() -> str:
    with SessionLocal() as session:
        users = session.query(UserModel).all()

        while True:
            user_id = generate_random_string(length=25)
            duplicate_found = False
            for user in users:
                if user.user_id == user_id:
                    duplicate_found = True
                    break

            if duplicate_found is False:
                return user_id


def generate_random_string(length) -> str:
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string
