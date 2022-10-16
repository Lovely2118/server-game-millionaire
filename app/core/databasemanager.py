import random
import string

from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.errors import UserIsNotInDatabase, LevelModelDoesNotExist, BlockModelDoesNotExist
from app.models.quiz_models import UserModel, LevelModel, BlockModel


class DatabaseManager:
    def get_user_by_user_id(self, user_id: str) -> UserModel:
        with SessionLocal() as session:
            user = self.__get_user_by_user_id(session, user_id)
            if user is None:
                raise UserIsNotInDatabase()
            return user

    def register_test_user(self, user_name: str, number_money: int, number_block: int) -> UserModel:
        """
            # TODO: используется строго для тестирования
        """
        with SessionLocal() as session:
            user_id = "test_user_id"
            all_blocks: list['BlockModel'] = session.query(BlockModel).all()
            selected_block = [block for block in all_blocks
                              if block.question == "Как называют погоду, когда температура опускается гораздо ниже нуля?" or
                              block.question == "Кем была девочка, которая несла бабушке пирожки в сказке «Красная шапочка»?"]

            new_user = UserModel(
                user_id=user_id,
                name=user_name,
                money=number_money,
                number_block=number_block,
                blocks=selected_block
            )
            return new_user

    def register_user(self, user_name: str) -> UserModel:
        with SessionLocal() as session:
            user_id = self.generate_unique_user_id()
            blocks = self.__get_blocks_of_one_game(session)
            new_user = UserModel(
                user_id=user_id,
                name=user_name,
                money=100,
                number_block=0,
                blocks=blocks
            )
            session.add(new_user)
            session.commit()
            return new_user

    def check_user_by_user_id(self, user_id: str) -> bool:
        with SessionLocal() as session:
            user = self.__get_user_by_user_id(session, user_id)
            return user is not None

    def generate_unique_user_id(self) -> str:
        with SessionLocal() as session:
            users = session.query(UserModel).all()

            while True:
                user_id = self.__generate_random_string(length=25)
                duplicate_found = False
                for user in users:
                    if user.user_id == user_id:
                        duplicate_found = True
                        break

                if duplicate_found is False:
                    return user_id

    @staticmethod
    def next_block(user: UserModel) -> bool:
        with SessionLocal() as session:
            max_blocks = len(user.blocks)
            current_block = user.number_block

            if current_block + 1 < max_blocks:
                user.number_block += 1
                session.add(user)
                session.commit()
                return False
            return True

    def reset_block(self, user: UserModel) -> None:
        with SessionLocal() as session:
            user.number_block = 0
            user.blocks = self.__get_blocks_of_one_game(session)
            session.add(user)
            session.commit()

    @staticmethod
    def __get_user_by_user_id(session: Session, user_id: str) -> UserModel | None:
        user = session.query(UserModel).filter(UserModel.user_id == user_id).first()
        return user

    def __get_blocks_of_one_game(self, session: Session) -> list['BlockModel']:
        """
            Генерирует 5 блоков вопроса/ответов для одной игры
        """
        level_1_blocks = self.__get_random_five_blocks_by_level(session, 0)
        level_2_blocks = self.__get_random_five_blocks_by_level(session, 1)
        level_3_blocks = self.__get_random_five_blocks_by_level(session, 2)
        level_4_blocks = self.__get_random_five_blocks_by_level(session, 3)
        level_5_blocks = self.__get_random_five_blocks_by_level(session, 4)
        return level_1_blocks + level_2_blocks + level_3_blocks + level_4_blocks + level_5_blocks

    def __get_random_five_blocks_by_level(self, session: Session, level: int) -> list['BlockModel']:
        result: list['BlockModel'] = []
        while len(result) != 5:
            random_block = self.__get_random_block_by_level(session, level)
            there_is_copy = False
            for ready_block in result:
                if ready_block.id == random_block.id:
                    there_is_copy = True
                    break

            if there_is_copy is False:
                result.append(random_block)
        return result

    @staticmethod
    def __get_random_block_by_level(session: Session, level: int) -> BlockModel:
        selected_level = session.query(LevelModel).filter(LevelModel.level == level).first()
        if selected_level is None:
            raise LevelModelDoesNotExist("There are no levels on the server")

        blocks_by_level = session.query(BlockModel).filter(BlockModel.level == selected_level).all()
        if blocks_by_level is None:
            raise BlockModelDoesNotExist("There are no blocks on the server")

        random_block = random.randint(0, len(blocks_by_level) - 1)
        return blocks_by_level[random_block]

    @staticmethod
    def __generate_random_string(length) -> str:
        letters = string.ascii_lowercase
        rand_string = ''.join(random.choice(letters) for i in range(length))
        return rand_string
