from app.core.utils import get_users, save_users
from app.core.utils import check_entry_in_list
from app.errors import UserAlreadyExists, FailedToReplaceUser, UserIsNotInJson
from app.schemes.base_schemas import User, Block


def add_user(user: User, users: list['User']) -> None:
    """
        Добавление нового пользователя в бд (json)
    :param users:
    :param user:
    :return:
    """
    is_uniqueness = check_uniqueness(user.user_id, users)
    if is_uniqueness:
        users.append(user)
        save_users(users)
        return

    raise UserAlreadyExists()


def go_to_next_question(user: User, level: list['Block']) -> None:
    """
        Перемещает пользователя на новый вопрос
    :param user:
    :param level:
    :return:
    """
    next_answer_id = user.number_question_in_block + 1
    if check_entry_in_list(next_answer_id, level):
        user.number_question_in_block = next_answer_id
    else:
        current_int_block = int(user.name_block[-1])
        if current_int_block + 1 < 5:
            current_int_block = current_int_block + 1
        user.name_block = f"level_{current_int_block}"
        user.number_question_in_block = 0
    update_user(user)


def go_to_first_question(user: User) -> None:
    """
        Сбрасывает вопросы пользователя до первого
    :param user:
    :return:
    """
    user.name_block = "level_1"
    user.number_question_in_block = 0
    update_user(user)


def update_user(user: User) -> None:
    """
        Обновление данных пользователя в бд (json)
    :param user:
    :return:
    """

    users = get_users()

    is_uniqueness = check_uniqueness(user.user_id, users)
    if is_uniqueness is False:
        replace_user(user, users)
        save_users(users)
        return

    raise UserIsNotInJson()


def get_user_by_id(user_id: str, users: list['User']) -> User:
    for user_from_bd in users:
        if user_from_bd.user_id == user_id:
            return user_from_bd

    raise UserIsNotInJson()


def check_uniqueness(user_id: str, users: list['User']) -> bool:
    for user_from_bd in users:
        if user_from_bd.user_id == user_id:
            return False
    return True


def replace_user(user: User, users: list['User']) -> None:
    selected_index = -1
    for index in range(len(users)):
        user_from_bd = users[index]
        if user_from_bd.user_id == user.user_id:
            selected_index = index
            break

    if selected_index == -1:
        raise FailedToReplaceUser()

    users[selected_index] = user
