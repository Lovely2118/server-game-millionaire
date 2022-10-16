import random
import string

from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.errors import UserIsNotInDatabase, LevelModelDoesNotExist, BlockModelDoesNotExist
from app.models.quiz_models import UserModel, LevelModel, BlockModel


def get_user_by_user_id(user_id: str) -> UserModel:
    with SessionLocal() as session:
        user = __get_user_by_user_id(session, user_id)
        if user is None:
            raise UserIsNotInDatabase()
        return user


def register_user(user_name: str) -> UserModel:
    with SessionLocal() as session:
        user_id = generate_unique_user_id()
        blocks = __get_blocks_of_one_game(session)
        new_user = UserModel(
            user_id=user_id,
            name=user_name,
            money=100,
            number_block=0,
            blocks=blocks
        )
        return new_user


def __get_user_by_user_id(session: Session, user_id: str) -> UserModel | None:
    user = session.query(UserModel).filter(UserModel.user_id == user_id).first()
    return user


def check_user_by_user_id(user_id: str) -> bool:
    with SessionLocal() as session:
        user = __get_user_by_user_id(session, user_id)
        return user is not None


def __get_blocks_of_one_game(session: Session) -> list['BlockModel']:
    """
        Генерирует 5 блоков вопроса/ответов для одной игры
    """
    level_1_blocks = __get_random_five_blocks_by_level(session, 0)
    level_2_blocks = __get_random_five_blocks_by_level(session, 1)
    level_3_blocks = __get_random_five_blocks_by_level(session, 2)
    level_4_blocks = __get_random_five_blocks_by_level(session, 3)
    level_5_blocks = __get_random_five_blocks_by_level(session, 4)
    return level_1_blocks + level_2_blocks + level_3_blocks + level_4_blocks + level_5_blocks


def __get_random_five_blocks_by_level(session: Session, level: int) -> list['BlockModel']:
    result: list['BlockModel'] = []
    while len(result) != 5:
        random_block = __get_random_block_by_level(session, level)
        there_is_copy = False
        for ready_block in result:
            if ready_block.id == random_block.id:
                there_is_copy = True
                break

        if there_is_copy is False:
            result.append(random_block)
    return result


def __get_random_block_by_level(session: Session, level: int) -> BlockModel:
    selected_level = session.query(LevelModel).filter(LevelModel.level == level).first()
    if selected_level is None:
        raise LevelModelDoesNotExist("There are no levels on the server")

    blocks_by_level = session.query(BlockModel).filter(BlockModel.level == selected_level).all()
    if blocks_by_level is None:
        raise BlockModelDoesNotExist("There are no blocks on the server")

    random_block = random.randint(0, len(blocks_by_level) - 1)
    return blocks_by_level[random_block]


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
